import pytest
import networkx as nx
import numpy as np
from src.matrix_module import get_adjacency_matrix, get_degree_matrix, validate_matrices

def test_matrices_path_graph():
    G = nx.path_graph(3) # Nodes 0, 1, 2. Edges (0,1), (1,2)
    A = get_adjacency_matrix(G)
    D = get_degree_matrix(G)
    
    assert A.shape == (3, 3)
    assert D.shape == (3, 3)
    
    # Check Symmetry
    assert np.allclose(A, A.T)
    
    # Check Degree matrix
    expected_D = np.diag([1, 2, 1])
    assert np.allclose(D, expected_D)
    
    # Validation function
    assert validate_matrices(G, A, D) == True

def test_matrices_empty_graph():
    G = nx.Graph()
    A = get_adjacency_matrix(G)
    D = get_degree_matrix(G)
    assert A.size == 0
    assert D.size == 0
