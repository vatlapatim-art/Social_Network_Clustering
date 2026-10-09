
import numpy as np

A = np.load("adjacency_matrix.npy")
D = np.load("degree_matrix.npy")
degrees = np.load("node_degrees.npy")

print("Adjacency matrix:", A.shape)
print("Degree matrix:", D.shape)
print("Number of node degrees:", len(degrees))

print("Adjacency matrix is symmetric:", np.array_equal(A, A.T))
print("Diagonal of A is zero:", np.all(np.diag(A) == 0))
print("Degree matrix is correct:", np.array_equal(D, np.diag(degrees)))
print("Degree values are correct:", np.array_equal(degrees, A.sum(axis=1)))
print("Total edges:", int(A.sum() // 2))
