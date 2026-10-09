import pytest
import networkx as nx
import numpy as np
from src.evaluation_module import evaluate_communities

def test_evaluate_communities():
    G = nx.path_graph(4) # 0-1-2-3
    labels = np.array([0, 0, 1, 1])
    
    results = evaluate_communities(G, labels)
    
    assert results["community_sizes"][0] == 2
    assert results["community_sizes"][1] == 2
    assert "modularity" in results
    assert isinstance(results["modularity"], float)

def test_ari():
    G = nx.path_graph(4)
    labels = np.array([0, 0, 1, 1])
    true_labels = np.array([0, 0, 1, 1])
    
    results = evaluate_communities(G, labels, true_labels)
    assert results["ari"] == 1.0 # Perfect match
