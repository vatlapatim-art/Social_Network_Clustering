import numpy as np
from sklearn.cluster import KMeans
from typing import List

def spectral_bisection(fiedler_vector: np.ndarray) -> np.ndarray:
    """
    Performs 2-community bisection based on the Fiedler vector signs.
    Nodes with value >= 0 go to community 0, others to community 1.
    """
    if fiedler_vector.size == 0:
        return np.array([])
    return (fiedler_vector >= 0).astype(int)

def spectral_clustering(eigenvectors: np.ndarray, num_communities: int, random_seed: int = 42) -> np.ndarray:
    """
    Performs spectral clustering for a specified number of communities.
    Uses the first k eigenvectors (excluding the constant first eigenvector if strictly needed,
    but standard spectral clustering on L often uses the first k eigenvectors).
    We use the first `num_communities` eigenvectors corresponding to the smallest eigenvalues.
    """
    if eigenvectors.size == 0 or num_communities < 2:
        return np.array([])
        
    n_nodes = eigenvectors.shape[0]
    if num_communities > n_nodes:
        raise ValueError(f"Number of communities ({num_communities}) cannot exceed number of nodes ({n_nodes}).")
        
    # Standard spectral clustering embedding uses the first k eigenvectors
    embedding = eigenvectors[:, :num_communities]
    
    # K-means clustering on the embedding rows
    kmeans = KMeans(n_clusters=num_communities, random_state=random_seed, n_init=10)
    labels = kmeans.fit_predict(embedding)
    
    return labels
