import networkx as nx
import numpy as np
from sklearn.metrics import adjusted_rand_score
from typing import Dict, Any

def evaluate_communities(G: nx.Graph, labels: np.ndarray, true_labels: np.ndarray = None) -> Dict[str, Any]:
    """
    Evaluates the detected communities.
    Calculates community sizes and graph modularity.
    """
    if len(labels) == 0 or G.number_of_nodes() == 0:
        return {"community_sizes": {}, "modularity": 0.0, "ari": None}
        
    unique_labels, counts = np.unique(labels, return_counts=True)
    community_sizes = dict(zip(unique_labels, counts))
    
    # Group nodes by label for modularity calculation
    communities = [set() for _ in range(len(unique_labels))]
    nodes = list(G.nodes())
    for idx, label in enumerate(labels):
        # We need to map the label to an index 0..k-1
        # np.unique returns sorted labels
        label_idx = np.where(unique_labels == label)[0][0]
        communities[label_idx].add(nodes[idx])
        
    # Calculate Modularity
    try:
        modularity = nx.community.modularity(G, communities)
    except Exception:
        modularity = 0.0
        
    # Compare with true labels if provided
    ari = None
    if true_labels is not None and len(true_labels) == len(labels):
        ari = adjusted_rand_score(true_labels, labels)
        
    return {
        "community_sizes": community_sizes,
        "modularity": modularity,
        "ari": ari
    }
