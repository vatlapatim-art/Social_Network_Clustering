import pytest
import numpy as np
import networkx as nx
from src.matrix_module import get_adjacency_matrix, get_degree_matrix
from src.laplacian_module import get_graph_laplacian, analyze_eigenvalues

def test_laplacian_properties():
    G = nx.cycle_graph(4)
    A = get_adjacency_matrix(G)
    D = get_degree_matrix(G)
    L = get_graph_laplacian(A, D)
    
    # Check L = D - A
    assert np.allclose(L, D - A)
    
    # Check Symmetry
    assert np.allclose(L, L.T)
    
    # Check row sums are zero
    assert np.allclose(L.sum(axis=1), np.zeros(4))

def test_eigenvalues_connected():
    G = nx.path_graph(3)
    A = get_adjacency_matrix(G)
    D = get_degree_matrix(G)
    L = get_graph_laplacian(A, D)
    
    results = analyze_eigenvalues(L)
    
    assert results["num_zero_eigenvalues"] == 1
    assert results["algebraic_connectivity"] > 1e-10
    
    # Nonnegative eigenvalues
    assert np.all(results["eigenvalues"] >= -1e-10)

def test_eigenvalues_disconnected():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (3, 4)]) # 2 components
    
    A = get_adjacency_matrix(G)
    D = get_degree_matrix(G)
    L = get_graph_laplacian(A, D)
    
    results = analyze_eigenvalues(L)
    assert results["num_zero_eigenvalues"] == 2
    assert results["algebraic_connectivity"] < 1e-10 # lambda_2 is 0
    assert results["fiedler_residual"] < 1e-10
