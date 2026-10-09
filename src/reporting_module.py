import pandas as pd
import numpy as np
from typing import List, Any

def export_node_assignments(node_ids: List[Any], labels: np.ndarray) -> str:
    """Creates a CSV string of node to community assignments."""
    df = pd.DataFrame({"Node_ID": node_ids, "Community": labels})
    return df.to_csv(index=False)

def export_matrix(matrix: np.ndarray, name: str = "Matrix") -> str:
    """Creates a CSV string of a matrix."""
    df = pd.DataFrame(matrix)
    return df.to_csv(index=False, header=False)
