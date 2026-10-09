import numpy as np
import scipy.linalg as la
from typing import Tuple, List, Dict, Any

def get_graph_laplacian(A: np.ndarray, D: np.ndarray) -> np.ndarray:
    """Calculates the standard combinatorial graph Laplacian L = D - A."""
    if A.size == 0 or D.size == 0:
        return np.array([])
    return D - A

def get_normalized_laplacian(A: np.ndarray, D: np.ndarray) -> np.ndarray:
    """Calculates the normalized graph Laplacian L_sym = I - D^(-1/2) A D^(-1/2)."""
    if A.size == 0 or D.size == 0:
        return np.array([])
    
    n = A.shape[0]
    D_inv_sqrt = np.zeros_like(D, dtype=float)
    
    for i in range(n):
        if D[i, i] > 0:
            D_inv_sqrt[i, i] = 1.0 / np.sqrt(D[i, i])
            
    I = np.eye(n)
    return I - D_inv_sqrt @ A @ D_inv_sqrt

def analyze_eigenvalues(L: np.ndarray) -> Dict[str, Any]:
    """Calculates and analyzes the eigenvalues and eigenvectors of L."""
    if L.size == 0:
        return {}
        
    # Ensure symmetry for numerical stability with eigh
    # L = (L + L.T) / 2
    
    # eigh returns eigenvalues in ascending order
    eigenvalues, eigenvectors = la.eigh(L)
    
    # Identify zero eigenvalues (tolerance 1e-10)
    zero_mask = np.abs(eigenvalues) < 1e-10
    num_zero_eigenvalues = np.sum(zero_mask)
    
    # Set effectively zero eigenvalues exactly to 0 for cleaner output
    eigenvalues[zero_mask] = 0.0
    
    # Calculate algebraic connectivity
    # It is the second smallest eigenvalue (index 1)
    if len(eigenvalues) > 1:
        algebraic_connectivity = eigenvalues[1]
    else:
        algebraic_connectivity = 0.0
        
    # Fiedler vector (eigenvector corresponding to the second smallest eigenvalue)
    fiedler_vector = eigenvectors[:, 1] if len(eigenvalues) > 1 else np.array([])
    
    # Validation: L * v = lambda * v for the Fiedler vector
    residual = 0.0
    if len(eigenvalues) > 1:
        expected = algebraic_connectivity * fiedler_vector
        actual = L @ fiedler_vector
        residual = np.linalg.norm(actual - expected)
        
    return {
        "eigenvalues": eigenvalues,
        "eigenvectors": eigenvectors,
        "num_zero_eigenvalues": num_zero_eigenvalues,
        "algebraic_connectivity": algebraic_connectivity,
        "fiedler_vector": fiedler_vector,
        "fiedler_residual": residual
    }
