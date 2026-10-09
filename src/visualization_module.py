import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from typing import Optional, List
import matplotlib as mpl

# OCEANIC PALETTE
C_DEEP_TEAL = "#103C42"
C_DARK_TEAL = "#174F52"
C_TURQUOISE = "#39C6B4"
C_SEA_GREEN = "#67D6A3"
C_CORAL = "#FF8066"
C_GOLD = "#E9B44C"
C_MINT = "#C4F1DF"
C_CREAM = "#F3E9D2"

COMMUNITY_COLORS = [C_TURQUOISE, C_CORAL, C_GOLD, C_SEA_GREEN, C_MINT]

def apply_oceanic_theme():
    plt.style.use('dark_background')
    mpl.rcParams.update({
        "figure.facecolor": C_DEEP_TEAL,
        "axes.facecolor": C_DEEP_TEAL,
        "axes.edgecolor": C_DARK_TEAL,
        "axes.labelcolor": C_MINT,
        "text.color": C_CREAM,
        "xtick.color": C_MINT,
        "ytick.color": C_MINT,
        "grid.color": C_DARK_TEAL,
        "grid.alpha": 0.7,
        "font.family": "sans-serif"
    })

def get_node_colors(labels: np.ndarray) -> list:
    if len(labels) == 0:
        return []
    unique_labels = np.unique(labels)
    color_map = {lbl: COMMUNITY_COLORS[i % len(COMMUNITY_COLORS)] for i, lbl in enumerate(unique_labels)}
    return [color_map[lbl] for lbl in labels]

def plot_network_3d(G: nx.Graph, labels: np.ndarray = None, title: str = "") -> go.Figure:
    """Generates an interactive 3D network visualization using Plotly."""
    # Compute 3D layout (using spring layout in 3 dims)
    pos_3d = nx.spring_layout(G, dim=3, seed=42)
    
    # Extract edge coordinates
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        x0, y0, z0 = pos_3d[edge[0]]
        x1, y1, z1 = pos_3d[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])
        
    edges_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=1.5, color=C_DARK_TEAL),
        hoverinfo='none',
        mode='lines'
    )
    
    # Extract node coordinates and info
    node_x = []
    node_y = []
    node_z = []
    node_text = []
    
    nodes = list(G.nodes())
    for node in nodes:
        x, y, z = pos_3d[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        
        deg = G.degree(node)
        comm = labels[nodes.index(node)] if labels is not None else "N/A"
        node_text.append(f"Node: {node}<br>Degree: {deg}<br>Community: {comm}")
        
    if labels is not None and len(labels) == G.number_of_nodes():
        node_colors = get_node_colors(labels)
    else:
        node_colors = [C_TURQUOISE] * G.number_of_nodes()
        
    nodes_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=False,
            color=node_colors,
            size=8,
            line=dict(width=1, color=C_CREAM)
        )
    )
    
    fig = go.Figure(data=[edges_trace, nodes_trace])
    fig.update_layout(
        title=dict(text=title, font=dict(color=C_CREAM, size=16)),
        paper_bgcolor=C_DEEP_TEAL,
        plot_bgcolor=C_DEEP_TEAL,
        margin=dict(l=0, r=0, b=0, t=40),
        showlegend=False,
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title="", showgrid=False, zeroline=False),
            yaxis=dict(showbackground=False, showticklabels=False, title="", showgrid=False, zeroline=False),
            zaxis=dict(showbackground=False, showticklabels=False, title="", showgrid=False, zeroline=False),
            bgcolor=C_DEEP_TEAL
        )
    )
    return fig

def plot_network(G: nx.Graph, labels: np.ndarray = None, pos: dict = None, title: str = "", show_labels: bool = True) -> plt.Figure:
    """Plots the network in 2D."""
    apply_oceanic_theme()
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if pos is None:
        pos = nx.spring_layout(G, seed=42)
        
    if labels is not None and len(labels) == G.number_of_nodes():
        node_colors = get_node_colors(labels)
    else:
        node_colors = [C_TURQUOISE] * G.number_of_nodes()
        
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=200, edgecolors=C_CREAM, linewidths=1.0)
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.4, edge_color=C_MINT)
    
    if show_labels:
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_family='sans-serif', font_color=C_CREAM)
    
    if title:
        ax.set_title(title, pad=15, fontsize=14, color=C_CREAM)
    
    ax.axis('off')
    fig.tight_layout()
    return fig

def plot_matrix_heatmap(matrix: np.ndarray, title: str = "", cmap: str = 'ocean') -> plt.Figure:
    """Plots a heatmap representation of a matrix."""
    apply_oceanic_theme()
    fig, ax = plt.subplots(figsize=(7, 6))
    
    cax = ax.imshow(matrix, cmap=cmap, interpolation='nearest')
    
    cbar = fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(colors=C_MINT)
    
    if title:
        ax.set_title(title, pad=15, fontsize=12)
        
    if matrix.shape[0] > 50:
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        ax.tick_params(axis='both', which='both', length=0)
        
    fig.tight_layout()
    return fig

def plot_eigenvalues(eigenvalues: np.ndarray, k: int = 15, title: str = "") -> plt.Figure:
    """Plots the smallest eigenvalues."""
    apply_oceanic_theme()
    fig, ax = plt.subplots(figsize=(8, 5))
    
    num_to_plot = min(k, len(eigenvalues))
    ax.plot(range(num_to_plot), eigenvalues[:num_to_plot], marker='o', markersize=6, 
            linestyle='-', color=C_TURQUOISE, linewidth=1.5, markerfacecolor=C_DEEP_TEAL)
            
    ax.set_xlabel('Index ($i$)', labelpad=10)
    ax.set_ylabel('Eigenvalue ($\lambda_i$)', labelpad=10)
    
    if title:
        ax.set_title(title, pad=15, fontsize=12)
        
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
    ax.set_xticks(range(num_to_plot))
    
    if num_to_plot > 0:
        ax.plot(0, eigenvalues[0], marker='o', markersize=8, color=C_CORAL) # Zero
    if num_to_plot > 1:
        ax.plot(1, eigenvalues[1], marker='o', markersize=8, color=C_GOLD) # Fiedler
        
    fig.tight_layout()
    return fig
