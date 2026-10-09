import networkx as nx
import pandas as pd
from typing import Tuple, Dict, Any, Optional

def load_karate_club_graph() -> nx.Graph:
    """Loads Zachary's Karate Club dataset from NetworkX."""
    return nx.karate_club_graph()

def load_graph_from_csv(file_path_or_buffer) -> nx.Graph:
    """Loads an unweighted, undirected graph from a CSV edge list."""
    try:
        df = pd.read_csv(file_path_or_buffer)
        if df.shape[1] < 2:
            raise ValueError("CSV must contain at least two columns for source and target nodes.")
        
        # Take the first two columns
        source_col, target_col = df.columns[0], df.columns[1]
        
        G = nx.Graph()
        for _, row in df.iterrows():
            u, v = row[source_col], row[target_col]
            if pd.notna(u) and pd.notna(v):
                if u != v: # Ignore self-loops for simple graph
                    G.add_edge(u, v)
        return G
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {e}")

def get_graph_statistics(G: nx.Graph) -> Dict[str, Any]:
    """Computes basic statistics for the graph."""
    if G.number_of_nodes() == 0:
        return {
            "num_nodes": 0,
            "num_edges": 0,
            "min_degree": 0,
            "max_degree": 0,
            "avg_degree": 0,
            "num_components": 0
        }
        
    degrees = [d for n, d in G.degree()]
    
    return {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "min_degree": min(degrees),
        "max_degree": max(degrees),
        "avg_degree": sum(degrees) / len(degrees),
        "num_components": nx.number_connected_components(G)
    }
