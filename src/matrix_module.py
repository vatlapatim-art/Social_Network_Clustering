import networkx as nx
import numpy as np
from typing import Tuple

def get_adjacency_matrix(G: nx.Graph) -> np.ndarray:
    """Creates the adjacency matrix A for the graph."""
    if G.number_of_nodes() == 0:
        return np.array([])
    return nx.adjacency_matrix(G, weight=None).toarray()

def get_degree_matrix(G: nx.Graph) -> np.ndarray:
    """Creates the degree matrix D for the graph."""
    if G.number_of_nodes() == 0:
        return np.array([])
    degrees = [d for n, d in G.degree()]
    return np.diag(degrees)

def validate_matrices(G: nx.Graph, A: np.ndarray, D: np.ndarray) -> bool:
    """Validates that A and D correctly represent the graph G."""
    n = G.number_of_nodes()
    
    # Check dimensions
    if A.shape != (n, n) or D.shape != (n, n):
        return False
        
    # A should be symmetric for an undirected graph
    if not np.allclose(A, A.T):
        return False
        
    # D should be diagonal
    if not np.allclose(D, np.diag(np.diagonal(D))):
        return False
        
    # D diagonal elements should match node degrees in order
    expected_degrees = np.array([d for n, d in G.degree()])
    if not np.allclose(np.diagonal(D), expected_degrees):
        return False
        
    return True
