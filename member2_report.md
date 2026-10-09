# Member 2 Report: Graph Laplacian, Eigenpairs and Fiedler Vector

**Dataset:** Zachary's Karate Club (34 nodes, 78 edges), loaded from Member 1's `adjacency_matrix.npy`.

## 1. The Laplacian L = D - A

- **A** is the adjacency matrix: A[i][j] = 1 if members i and j are connected, otherwise 0.
- **D** is the diagonal degree matrix: D[i][i] is the number of connections of node i (the row sum of A).
- **L = D - A** is the graph Laplacian. Its diagonal holds each node's degree and each off-diagonal entry is -1 for a connected pair, so every row sums to 0.

Properties confirmed on this dataset:
- L is symmetric and every row sum is 0.
- The smallest eigenvalue is 0 (numerically about -3e-16), with the all-ones vector as its eigenvector.
- The eigenvalues add up to trace(L) = 2 x 78 = 156.
- My L matches Member 1's `laplacian_matrix.npy` exactly.

## 2. Eigenvalues and eigenvectors

`np.linalg.eigh(L)` returns the 34 eigenvalues in ascending order, with the eigenvectors as the columns of a 34 x 34 matrix. All eigenvalues are >= 0, as expected for a Laplacian. The full lists are in `laplacian_eigenvalues.npy` and `laplacian_eigenvectors.npy`.

## 3. Fiedler value and vector

- **Fiedler value (2nd smallest eigenvalue): 0.4685.** It is greater than 0, so the graph is **connected**. If the graph were disconnected, this value would be 0.
- **Fiedler vector:** the eigenvector for that eigenvalue, saved in `fiedler_vector.npy` and printed in `member2_output.txt`.
- **Interpretation:** the sign of each entry splits the members into two groups. Group A (>= 0) has 19 nodes and Group B (< 0) has 15. This matches the club's real split into Mr. Hi's and the Officer's factions for 32 of 34 members (94.1%). The two disagreements are nodes 2 and 8, the members known to sit between the two groups.

## 4. Validation

| Check | Result |
|---|---|
| ‖L v - λ v‖ for the Fiedler pair | 4.2e-15 |
| Max error over all 34 eigenpairs | 3.0e-14 |
| Number of zero eigenvalues (connected components) | 1 (connected graph) |
| Row sums of L equal 0 | True |
| L symmetric | True |

The error is at the level of machine precision, so the eigendecomposition is correct.
