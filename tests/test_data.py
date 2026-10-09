import pytest
import networkx as nx
import pandas as pd
import io
from src.data_module import load_karate_club_graph, get_graph_statistics, load_graph_from_csv

def test_load_karate_club():
    G = load_karate_club_graph()
    assert G.number_of_nodes() == 34
    assert G.number_of_edges() == 78

def test_graph_statistics():
    G = nx.path_graph(3)
    stats = get_graph_statistics(G)
    assert stats["num_nodes"] == 3
    assert stats["num_edges"] == 2
    assert stats["min_degree"] == 1
    assert stats["max_degree"] == 2
    assert stats["num_components"] == 1

def test_empty_graph_stats():
    G = nx.Graph()
    stats = get_graph_statistics(G)
    assert stats["num_nodes"] == 0
    assert stats["num_edges"] == 0

def test_load_csv():
    csv_data = "source,target\n1,2\n2,3\n3,1\n"
    G = load_graph_from_csv(io.StringIO(csv_data))
    assert G.number_of_nodes() == 3
    assert G.number_of_edges() == 3
