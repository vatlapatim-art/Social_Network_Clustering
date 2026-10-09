"""
Member 2: Graph Laplacian, eigenvalues/eigenvectors and Fiedler pair.

Uses the files produced by Member 1 (person1.py):
    adjacency_matrix.npy, degree_matrix.npy, laplacian_matrix.npy (optional check)

Run order:
    python person1.py                      # Member 1 -> creates adjacency_matrix.npy etc.
    python member2_laplacian_analysis.py   # Member 2 -> this file
"""
import os
import numpy as np
import networkx as nx

from laplacian_module import (
    calculate_laplacian,
    calculate_eigenpairs,
    get_fiedler_pair,
)

np.set_printoptions(precision=4, suppress=True, linewidth=120)

# ---------------------------------------------------------------- load data
A = np.load("adjacency_matrix.npy")
n = A.shape[0]
print("Loaded adjacency matrix:", A.shape, "| edges:", int(A.sum() // 2))

# ------------------------------------------------- degree matrix + Laplacian
D, L = calculate_laplacian(A)

print("\nDegree matrix D (first 5 x 5):\n", D[:5, :5])
print("\nGraph Laplacian L = D - A (first 5 x 5):\n", L[:5, :5])

# Cross-check against Member 1's saved matrices
if os.path.exists("degree_matrix.npy"):
    print("\nMy D matches Member 1's D:", np.allclose(D, np.load("degree_matrix.npy")))
if os.path.exists("laplacian_matrix.npy"):
    print("My L matches Member 1's L:", np.allclose(L, np.load("laplacian_matrix.npy")))

# ------------------------------------------------------ eigen decomposition
eigenvalues, eigenvectors = calculate_eigenpairs(L)
fiedler_value, fiedler_vector = get_fiedler_pair(eigenvalues, eigenvectors)

print("\nEigenvalues (ascending):\n", eigenvalues)
print("\nEigenvectors matrix shape:", eigenvectors.shape, "(each column is one eigenvector)")
print("\nFiedler value (2nd smallest eigenvalue):", fiedler_value)
print("Fiedler vector:\n", fiedler_vector)

# ---------------------------------------------------------------- validation
error = np.linalg.norm(L @ fiedler_vector - fiedler_value * fiedler_vector)
error_all = np.linalg.norm(L @ eigenvectors - eigenvectors * eigenvalues)
zero_count = int(np.sum(eigenvalues < 1e-10))

print("\n--- Validation ---")
print("Eigenvector validation error ||L v - lambda v||:", error)
print("Max error over ALL eigenpairs:", error_all)
print("L is symmetric:", np.allclose(L, L.T))
print("Row sums of L are zero:", np.allclose(L.sum(axis=1), 0))
print("Smallest eigenvalue (should be ~0):", eigenvalues[0])
print("Sum of eigenvalues = trace(L) = 2*edges:", eigenvalues.sum(), "vs", np.trace(L))
print("Number of zero eigenvalues (= connected components):", zero_count)
if zero_count > 1:
    print("NOTE: the graph is DISCONNECTED, so the Fiedler value is ~0.")
else:
    print("The graph is connected, so the Fiedler value is > 0.")

# ------------------------------------- interpretation: two-way split of nodes
group_a = np.where(fiedler_vector >= 0)[0]
group_b = np.where(fiedler_vector < 0)[0]
print("\nFiedler sign partition:")
print("  Group A (v >= 0):", group_a.tolist())
print("  Group B (v <  0):", group_b.tolist())

# Compare with the known real-world split of the karate club (Mr. Hi vs Officer)
G = nx.karate_club_graph()
truth = np.array([0 if G.nodes[i]["club"] == "Mr. Hi" else 1 for i in range(n)])
pred = (fiedler_vector >= 0).astype(int)
acc = max(np.mean(pred == truth), np.mean(pred != truth))  # sign of eigenvector is arbitrary
print(f"Agreement with the real club split: {acc * 100:.1f}% ({int(round(acc * n))}/{n} members)")

# ------------------------------------------------------------------ save
np.save("laplacian_eigenvalues.npy", eigenvalues)
np.save("laplacian_eigenvectors.npy", eigenvectors)
np.save("fiedler_vector.npy", fiedler_vector)
print("\nSaved laplacian_eigenvalues.npy, laplacian_eigenvectors.npy, fiedler_vector.npy")
