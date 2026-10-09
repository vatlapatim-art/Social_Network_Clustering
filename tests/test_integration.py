import pytest
from src.data_module import load_karate_club_graph
from src.matrix_module import get_adjacency_matrix, get_degree_matrix
from src.laplacian_module import get_graph_laplacian, analyze_eigenvalues
from src.spectral_module import spectral_clustering
from src.evaluation_module import evaluate_communities

def test_full_pipeline():
    # 1. Load Data
    G = load_karate_club_graph()
    
    # 2. Matrices
    A = get_adjacency_matrix(G)
    D = get_degree_matrix(G)
    
    # 3. Laplacian & Eigenvalues
    L = get_graph_laplacian(A, D)
    eigen_results = analyze_eigenvalues(L)
    
    # 4. Clustering
    labels = spectral_clustering(eigen_results["eigenvectors"], num_communities=2)
    
    # 5. Evaluation
    eval_results = evaluate_communities(G, labels)
    
    # Assertions
    assert len(labels) == 34
    assert eval_results["modularity"] > 0
    assert eigen_results["algebraic_connectivity"] > 0 # Karate club is connected
