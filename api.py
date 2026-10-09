from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx
import numpy as np
from typing import List, Optional

# Import existing math modules
from src.data_module import load_karate_club_graph, get_graph_statistics
from src.matrix_module import get_adjacency_matrix, get_degree_matrix, validate_matrices
from src.laplacian_module import get_graph_laplacian, analyze_eigenvalues
from src.spectral_module import spectral_clustering
from src.evaluation_module import evaluate_communities

app = FastAPI(title="Social Network Clustering API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

G = load_karate_club_graph()
A = get_adjacency_matrix(G)
D = get_degree_matrix(G)
L = get_graph_laplacian(A, D)
eigen_res = analyze_eigenvalues(L)

class ClusterRequest(BaseModel):
    num_communities: int
    random_seed: int = 42

@app.get("/api/network")
def get_network():
    if G.number_of_nodes() == 0:
        return {"nodes": [], "edges": []}
    pos_3d = nx.spring_layout(G, dim=3, seed=42)
    pos_2d = nx.spring_layout(G, dim=2, seed=42)
    nodes = []
    for n in G.nodes():
        nodes.append({
            "id": n,
            "degree": G.degree(n),
            "x": float(pos_3d[n][0]), "y": float(pos_3d[n][1]), "z": float(pos_3d[n][2]),
            "x2d": float(pos_2d[n][0]), "y2d": float(pos_2d[n][1])
        })
    edges = [{"source": u, "target": v} for u, v in G.edges()]
    return {"nodes": nodes, "edges": edges}

@app.get("/api/statistics")
def get_statistics():
    stats = get_graph_statistics(G)
    stats["density"] = nx.density(G)
    stats["clustering_coefficient"] = nx.average_clustering(G)
    
    # Path length only valid for connected graphs
    if nx.is_connected(G):
        stats["avg_shortest_path"] = nx.average_shortest_path_length(G)
    else:
        stats["avg_shortest_path"] = None
        
    stats["degree_dist"] = [d for n, d in G.degree()]
    return stats

@app.get("/api/centrality")
def get_centrality():
    return {
        "degree": nx.degree_centrality(G),
        "betweenness": nx.betweenness_centrality(G),
        "closeness": nx.closeness_centrality(G)
    }

@app.get("/api/path")
def get_shortest_path(source: int, target: int):
    try:
        path = nx.shortest_path(G, source=source, target=target)
        edges = [{"source": path[i], "target": path[i+1]} for i in range(len(path)-1)]
        return {"path": path, "edges": edges, "length": len(path)-1}
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return {"path": [], "edges": [], "length": 0}

@app.get("/api/matrices")
def get_matrices():
    return {
        "adjacency": A.tolist(),
        "degree": np.diagonal(D).tolist(),
        "laplacian": L.tolist(),
        "n": G.number_of_nodes()
    }

@app.get("/api/eigenvalues")
def get_eigenvalues():
    return {
        "eigenvalues": eigen_res.get("eigenvalues", []).tolist(),
        "algebraic_connectivity": float(eigen_res.get("algebraic_connectivity", 0)),
        "fiedler_vector": eigen_res.get("fiedler_vector", []).tolist()
    }

@app.post("/api/cluster")
def cluster_network(req: ClusterRequest):
    if req.num_communities < 2:
        raise HTTPException(status_code=400, detail="Must have at least 2 communities.")
    labels = spectral_clustering(eigen_res["eigenvectors"], req.num_communities, req.random_seed)
    true_labels = np.array([1 if G.nodes[n].get('club') == 'Officer' else 0 for n in G.nodes()])
    eval_res = evaluate_communities(G, labels, true_labels)
    node_labels = {str(n): int(labels[i]) for i, n in enumerate(G.nodes())}
    return {
        "labels": node_labels,
        "modularity": float(eval_res["modularity"]),
        "ari": float(eval_res["ari"]) if eval_res["ari"] is not None else None,
        "community_sizes": {str(k): int(v) for k, v in eval_res["community_sizes"].items()}
    }

