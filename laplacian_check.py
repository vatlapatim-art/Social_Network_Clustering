
import numpy as np

A = np.load("adjacency_matrix.npy")
D = np.load("degree_matrix.npy")

L = D - A

print("Laplacian shape:", L.shape)
print("Laplacian is symmetric:", np.allclose(L, L.T))
print("Row sums are zero:", np.allclose(L.sum(axis=1), 0))

np.save("laplacian_matrix.npy", L)
print("Saved laplacian_matrix.npy")
