import numpy as np


def calculate_laplacian(A):
    """Calculate the degree matrix D and Laplacian L = D - A."""

    A = np.asarray(A, dtype=float)

    # Basic checks
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("Adjacency matrix must be square.")

    if not np.allclose(A, A.T):
        raise ValueError("This code expects an undirected graph.")

    # Degree matrix and graph Laplacian
    degrees = A.sum(axis=1)
    D = np.diag(degrees)
    L = D - A

    return D, L


def calculate_eigenpairs(L):
    """Calculate eigenvalues and eigenvectors in ascending order."""

    eigenvalues, eigenvectors = np.linalg.eigh(L)
    return eigenvalues, eigenvectors


def get_fiedler_pair(eigenvalues, eigenvectors):
    """Return the second-smallest eigenvalue and its eigenvector."""

    if len(eigenvalues) < 2:
        raise ValueError("At least two nodes are required.")

    fiedler_value = eigenvalues[1]
    fiedler_vector = eigenvectors[:, 1]

    return fiedler_value, fiedler_vector
