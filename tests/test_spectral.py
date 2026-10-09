import pytest
import numpy as np
from src.spectral_module import spectral_bisection, spectral_clustering

def test_spectral_bisection():
    fiedler_vector = np.array([-0.5, -0.1, 0.2, 0.6])
    labels = spectral_bisection(fiedler_vector)
    
    expected = np.array([0, 0, 1, 1])
    assert np.array_equal(labels, expected)

def test_spectral_clustering():
    # Mock eigenvectors
    # Nodes 1, 2 are similar. Nodes 3, 4 are similar.
    eigenvectors = np.array([
        [0.5, 0.5],
        [0.5, 0.4],
        [0.5, -0.5],
        [0.5, -0.4]
    ])
    
    labels = spectral_clustering(eigenvectors, num_communities=2, random_seed=42)
    assert len(labels) == 4
    
    # Node 0 and 1 should have same label, 2 and 3 should have same label
    assert labels[0] == labels[1]
    assert labels[2] == labels[3]
    assert labels[0] != labels[2]

def test_invalid_num_communities():
    eigenvectors = np.array([[1.0], [1.0]])
    with pytest.raises(ValueError):
        spectral_clustering(eigenvectors, num_communities=5)
