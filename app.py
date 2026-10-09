import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.data_module import load_karate_club_graph, load_graph_from_csv, get_graph_statistics
from src.matrix_module import get_adjacency_matrix, get_degree_matrix, validate_matrices
from src.laplacian_module import get_graph_laplacian, analyze_eigenvalues
from src.spectral_module import spectral_bisection, spectral_clustering
from src.evaluation_module import evaluate_communities
from src.visualization_module import plot_network, plot_matrix_heatmap, plot_eigenvalues, plot_network_3d
from src.reporting_module import export_node_assignments, export_matrix

st.set_page_config(page_title="Social Network Lab", layout="wide", initial_sidebar_state="expanded")

# --- OCEANIC UI/UX THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    /* Main Backgrounds */
    .stApp {
        background-color: #103C42; /* Deep Ocean Teal */
        color: #F3E9D2; /* Warm Cream */
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #174F52; /* Dark Teal */
        border-right: 1px solid rgba(196, 241, 223, 0.2);
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #F3E9D2 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Metric Cards / Panels with Depth */
    div[data-testid="metric-container"], .ocean-panel {
        background: linear-gradient(145deg, #12434A, #0E353B);
        border: 1px solid rgba(57, 198, 180, 0.2); /* Turquoise subtle border */
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="metric-container"] label {
        color: #C4F1DF !important; /* Soft Mint */
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #39C6B4 !important; /* Turquoise */
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 1px solid rgba(57, 198, 180, 0.3);
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #C4F1DF;
        transition: color 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #39C6B4 !important;
        border-bottom: 2px solid #39C6B4 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #174F52;
        color: #F3E9D2;
        border: 1px solid #39C6B4;
        border-radius: 6px;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #39C6B4;
        color: #103C42;
        box-shadow: 0 4px 12px rgba(57, 198, 180, 0.4);
    }
    
    /* Dataframes / Tables */
    .stDataFrame {
        font-family: 'Consolas', 'Courier New', monospace;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #174F52;
        border: 1px solid rgba(57, 198, 180, 0.3);
        color: #F3E9D2;
        border-radius: 6px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(196, 241, 223, 0.2) !important;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    /* Labels */
    .stRadio label, .stSelectbox label, .stSlider label {
        color: #C4F1DF !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🌊 SOCIAL NETWORK LAB")
    st.markdown("<p style='color: #C4F1DF; font-size: 0.85rem; margin-top: -10px; margin-bottom: 30px;'>Immersive Graph Analytics</p>", unsafe_allow_html=True)
    
    page = st.radio("NAVIGATION", [
        "01  Overview",
        "02  Network Explorer",
        "03  Community Detection",
        "04  Matrix Analysis",
        "05  Eigenvalue Analysis",
        "06  Evaluation",
        "07  About the Project"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    
    st.markdown("<p style='color: #C4F1DF; font-size: 0.8rem; text-transform: uppercase; font-weight: 600;'>Dataset Configuration</p>", unsafe_allow_html=True)
    dataset_choice = st.radio("Select Dataset", ["Zachary's Karate Club", "Upload CSV (Edge List)"], label_visibility="collapsed")
    
    uploaded_csv = None
    if dataset_choice == "Upload CSV (Edge List)":
        uploaded_csv = st.file_uploader("Upload CSV", type=["csv"])
        
    st.markdown("---")
    st.markdown("<p style='color: #67D6A3; font-size: 0.75rem;'>v2.0.0 • PES University</p>", unsafe_allow_html=True)

# --- DATA LOADING & CACHING ---
@st.cache_data
def load_data(choice, uploaded_file=None):
    if choice == "Zachary's Karate Club":
        return load_karate_club_graph()
    elif choice == "Upload CSV (Edge List)" and uploaded_file is not None:
        try:
            return load_graph_from_csv(uploaded_file)
        except Exception as e:
            return None
    return None

G = load_data(dataset_choice, uploaded_csv)

if G is None:
    st.title("Data Required")
    st.info("Please load a valid dataset in the sidebar to begin analysis.")
    st.stop()

# --- COMPUTATION (Cached per parameters) ---
@st.cache_data
def compute_analysis(_G, num_comms, r_seed, use_fiedler):
    stats = get_graph_statistics(_G)
    nodes = list(_G.nodes())
    A = get_adjacency_matrix(_G)
    D = get_degree_matrix(_G)
    is_valid = validate_matrices(_G, A, D)
    L = get_graph_laplacian(A, D)
    eigen = analyze_eigenvalues(L)
    
    labels = None
    if stats["num_nodes"] > 0:
        if use_fiedler:
             labels = spectral_bisection(eigen["fiedler_vector"])
        else:
             labels = spectral_clustering(eigen["eigenvectors"], num_comms, r_seed)
             
    pos = nx.spring_layout(_G, seed=r_seed)
    
    true_labels = None
    if dataset_choice == "Zachary's Karate Club":
        true_labels = np.array([1 if _G.nodes[n]['club'] == 'Officer' else 0 for n in _G.nodes()])
        
    eval_res = evaluate_communities(_G, labels, true_labels)
    
    return stats, nodes, A, D, L, eigen, labels, pos, eval_res, is_valid

# Global config state
if "num_comms" not in st.session_state:
    st.session_state.num_comms = 2
if "r_seed" not in st.session_state:
    st.session_state.r_seed = 42
if "use_fiedler" not in st.session_state:
    st.session_state.use_fiedler = False

stats, nodes, A, D, L, eigen_results, labels, pos, eval_results, is_valid = compute_analysis(
    G, 
    st.session_state.num_comms, 
    st.session_state.r_seed, 
    st.session_state.use_fiedler and st.session_state.num_comms == 2 and dataset_choice == "Zachary's Karate Club"
)

# --- PAGE ROUTING ---

if page.startswith("01"):
    st.title("Network Overview")
    st.markdown("<p style='color: #C4F1DF; font-size: 1.1rem; margin-top: -10px;'>A high-level summary of the network topology.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nodes", stats["num_nodes"])
    c2.metric("Edges", stats["num_edges"])
    c3.metric("Components", stats["num_components"])
    c4.metric("Communities", len(np.unique(labels)) if labels is not None else 0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<span style='font-size: 0.85rem; text-transform: uppercase; color: #39C6B4; font-weight: 600;'>Immersive 3D Preview</span>", unsafe_allow_html=True)
        fig_3d = plot_network_3d(G, title="")
        st.plotly_chart(fig_3d, use_container_width=True)
        
    with col2:
        st.markdown("<span style='font-size: 0.85rem; text-transform: uppercase; color: #39C6B4; font-weight: 600;'>Topological Summary</span>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='ocean-panel' style='margin-top: 10px;'>
            <p style='margin: 8px 0;'><span style='color: #C4F1DF;'>Average Degree:</span> <strong style='float: right; color: #FF8066;'>{stats['avg_degree']:.2f}</strong></p>
            <p style='margin: 8px 0;'><span style='color: #C4F1DF;'>Min Degree:</span> <strong style='float: right; color: #F3E9D2;'>{stats['min_degree']}</strong></p>
            <p style='margin: 8px 0;'><span style='color: #C4F1DF;'>Max Degree:</span> <strong style='float: right; color: #F3E9D2;'>{stats['max_degree']}</strong></p>
            <hr style='margin: 15px 0; border-color: rgba(196, 241, 223, 0.2);'>
            <p style='margin: 8px 0;'><span style='color: #C4F1DF;'>Clustering Target:</span> <strong style='float: right; color: #E9B44C;'>{st.session_state.num_comms} communities</strong></p>
            <p style='margin: 8px 0;'><span style='color: #C4F1DF;'>Analysis Method:</span> <strong style='float: right; color: #F3E9D2;'>{'Fiedler Bisection' if st.session_state.use_fiedler and st.session_state.num_comms==2 else 'Spectral k-means'}</strong></p>
        </div>
        """, unsafe_allow_html=True)

elif page.startswith("02"):
    st.title("Interactive Network Explorer")
    st.markdown("<p style='color: #C4F1DF; font-size: 1.1rem; margin-top: -10px;'>Navigate the 3D topology of the social graph.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("<span style='font-size: 0.85rem; text-transform: uppercase; color: #39C6B4; font-weight: 600;'>Controls</span>", unsafe_allow_html=True)
        view_mode = st.radio("Color Scheme", ["Original", "Detected Communities"])
        
        st.markdown("<br><span style='font-size: 0.85rem; text-transform: uppercase; color: #39C6B4; font-weight: 600;'>Node Inspector</span>", unsafe_allow_html=True)
        selected = st.selectbox("Search / Highlight Node", nodes)
        if selected is not None:
            idx = nodes.index(selected)
            deg = G.degree(selected)
            comm = labels[idx] if labels is not None else "N/A"
            neigh = list(G.neighbors(selected))
            
            st.markdown(f"""
            <div class='ocean-panel'>
                <span style='color: #C4F1DF;'>ID:</span> <strong style='color: #F3E9D2;'>{selected}</strong><br>
                <span style='color: #C4F1DF;'>Degree:</span> <strong style='color: #FF8066;'>{deg}</strong><br>
                <span style='color: #C4F1DF;'>Community:</span> <strong style='color: #E9B44C;'>{comm}</strong><br>
                <br>
                <span style='color: #C4F1DF;'>Neighbors ({len(neigh)}):</span><br>
                <span style='color: #67D6A3; word-break: break-all; font-family: monospace;'>{', '.join(map(str, neigh))}</span>
            </div>
            """, unsafe_allow_html=True)

    with col1:
        if view_mode == "Original":
            fig_3d = plot_network_3d(G, title="")
        else:
            fig_3d = plot_network_3d(G, labels=labels, title="")
        st.plotly_chart(fig_3d, use_container_width=True, height=600)

elif page.startswith("03"):
    st.title("Community Detection")
    st.markdown("<p style='color: #C4F1DF; font-size: 1.1rem; margin-top: -10px;'>Spectral clustering partitions using Laplacian embeddings.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    cfg1, cfg2, cfg3, cfg4 = st.columns(4)
    with cfg1:
        st.session_state.num_comms = st.selectbox("Cluster Count ($k$)", [2, 3, 4], index=[2,3,4].index(st.session_state.num_comms))
    with cfg2:
        st.session_state.r_seed = st.number_input("Random Seed", value=st.session_state.r_seed, step=1)
    with cfg3:
        if dataset_choice == "Zachary's Karate Club" and st.session_state.num_comms == 2:
            st.session_state.use_fiedler = st.checkbox("Use Fiedler Sign Bisection", value=st.session_state.use_fiedler)
        else:
            st.session_state.use_fiedler = False
            st.markdown("<div style='margin-top: 35px; color: #C4F1DF; font-size: 0.8rem;'>Method: Spectral k-means</div>", unsafe_allow_html=True)
    with cfg4:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Apply Parameters", use_container_width=True):
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # Use tabs for 3D vs 2D viewing of communities
        tab_3d, tab_2d = st.tabs(["3D Interactive View", "2D Orthographic View"])
        with tab_3d:
            fig_3d = plot_network_3d(G, labels=labels, title="")
            st.plotly_chart(fig_3d, use_container_width=True)
        with tab_2d:
            fig_2d = plot_network(G, labels=labels, pos=pos, show_labels=True)
            st.pyplot(fig_2d)
            plt.close(fig_2d)
        
    with col2:
        st.markdown("<span style='font-size: 0.85rem; text-transform: uppercase; color: #39C6B4; font-weight: 600;'>Community Membership</span>", unsafe_allow_html=True)
        
        # Build dataframe for summary
        df_comm = pd.DataFrame({"Node": nodes, "Community": labels})
        summary = df_comm.groupby("Community").count().rename(columns={"Node": "Count"})
        summary["Percentage"] = (summary["Count"] / len(nodes) * 100).round(1).astype(str) + "%"
        
        st.dataframe(summary, use_container_width=True)
        
        st.markdown("<br><span style='font-size: 0.85rem; text-transform: uppercase; color: #39C6B4; font-weight: 600;'>Export Assignments</span>", unsafe_allow_html=True)
        csv_labels = export_node_assignments(nodes, labels)
        st.download_button("Download CSV", csv_labels, "community_assignments.csv", "text/csv", use_container_width=True)

elif page.startswith("04"):
    st.title("Matrix Analysis")
    st.markdown("<p style='color: #C4F1DF; font-size: 1.1rem; margin-top: -10px;'>Numerical representations of graph topology.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Adjacency Matrix (A)", "Degree Matrix (D)", "Graph Laplacian (L)"])
    
    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("#### Adjacency Matrix $A$")
            st.markdown("<p style='color: #C4F1DF;'>A symmetric matrix denoting edges. $A_{ij} = 1$ if an edge exists, else $0$.</p>", unsafe_allow_html=True)
            st.download_button("Export A (CSV)", export_matrix(A), "adjacency.csv", "text/csv")
        with c2:
            if stats["num_nodes"] <= 150:
                fig = plot_matrix_heatmap(A, cmap="ocean")
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.info("Matrix too large for heatmap preview.")
                
    with tab2:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("#### Degree Matrix $D$")
            st.markdown("<p style='color: #C4F1DF;'>A diagonal matrix where $D_{ii}$ equals the degree of node $i$.</p>", unsafe_allow_html=True)
            st.download_button("Export D (CSV)", export_matrix(D), "degree.csv", "text/csv")
        with c2:
            if stats["num_nodes"] <= 150:
                fig = plot_matrix_heatmap(D, cmap="ocean")
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.info("Matrix too large for heatmap preview.")

    with tab3:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("#### Graph Laplacian $L$")
            st.markdown("$L = D - A$")
            st.markdown(f"<p style='color: #67D6A3;'>*Integrity Check Valid: **{is_valid}***</p>", unsafe_allow_html=True)
            st.download_button("Export L (CSV)", export_matrix(L), "laplacian.csv", "text/csv")
        with c2:
            if stats["num_nodes"] <= 150:
                fig = plot_matrix_heatmap(L, cmap="coolwarm")
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.info("Matrix too large for heatmap preview.")

elif page.startswith("05"):
    st.title("Eigenvalue Analysis")
    st.markdown("<p style='color: #C4F1DF; font-size: 1.1rem; margin-top: -10px;'>Spectral properties of the Graph Laplacian.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Zero Eigenvalues", eigen_results.get("num_zero_eigenvalues", 0))
    c2.metric("Algebraic Connectivity", f"{eigen_results.get('algebraic_connectivity', 0):.4f}")
    c3.metric("Equation Residual $||Lv - \lambda v||$", f"{eigen_results.get('fiedler_residual', 0):.2e}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<span style='font-size: 0.85rem; text-transform: uppercase; color: #39C6B4; font-weight: 600;'>Smallest Eigenvalues</span>", unsafe_allow_html=True)
        fig = plot_eigenvalues(eigen_results.get("eigenvalues", []), k=15)
        st.pyplot(fig)
        plt.close(fig)
        
    with col2:
        st.markdown("<span style='font-size: 0.85rem; text-transform: uppercase; color: #39C6B4; font-weight: 600;'>Fiedler Vector (v₂)</span>", unsafe_allow_html=True)
        st.markdown("<p style='color: #C4F1DF; font-size: 0.85rem;'>Provides a 1-dimensional embedding that minimally cuts edges.</p>", unsafe_allow_html=True)
        if len(eigen_results.get("fiedler_vector", [])) > 0:
            df_fiedler = pd.DataFrame({
                "Node": nodes, 
                "Value": np.round(eigen_results["fiedler_vector"], 6)
            })
            st.dataframe(df_fiedler, use_container_width=True, height=350)
            st.download_button("Export Eigenvalues", pd.DataFrame(eigen_results["eigenvalues"]).to_csv(index=False, header=["Eigenvalue"]), "eigenvalues.csv", "text/csv", use_container_width=True)

elif page.startswith("06"):
    st.title("Evaluation")
    st.markdown("<p style='color: #C4F1DF; font-size: 1.1rem; margin-top: -10px;'>Quantitative assessment of community structure.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### Modularity")
        st.markdown("<p style='color: #C4F1DF; font-size: 0.9rem;'>Measures the density of edges inside communities compared to random connections.</p>", unsafe_allow_html=True)
        
        mod_val = eval_results['modularity']
        color = "#67D6A3" if mod_val > 0.3 else "#E9B44C" if mod_val > 0.1 else "#FF8066"
        st.markdown(f"""
        <div class='ocean-panel' style='text-align: center;'>
            <h1 style='color: {color} !important; font-size: 3rem; margin: 0;'>{mod_val:.4f}</h1>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("### Adjusted Rand Index")
        st.markdown("<p style='color: #C4F1DF; font-size: 0.9rem;'>Compares detected communities with known ground-truth labels.</p>", unsafe_allow_html=True)
        
        ari_val = eval_results['ari']
        if ari_val is not None:
            color = "#67D6A3" if ari_val > 0.7 else "#E9B44C" if ari_val > 0.3 else "#FF8066"
            st.markdown(f"""
            <div class='ocean-panel' style='text-align: center;'>
                <h1 style='color: {color} !important; font-size: 3rem; margin: 0;'>{ari_val:.4f}</h1>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='ocean-panel' style='text-align: center; opacity: 0.7;'>
                <h1 style='color: #9AA1A9 !important; font-size: 3rem; margin: 0;'>N/A</h1>
                <p style='color: #C4F1DF; font-size: 0.8rem; margin: 0;'>Ground truth unavailable.</p>
            </div>
            """, unsafe_allow_html=True)

elif page.startswith("07"):
    st.title("About the Project")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("""
    **Immersive 3D Social Network Community Detection**
    
    This application transforms mathematical graph analysis into a beautiful, immersive, interactive experience, demonstrating the power of Linear Algebra.
    
    ### Mathematical Pipeline
    1. **Graph Representation**: A social network is converted into an Adjacency Matrix ($A$).
    2. **Degree Normalization**: The connections per node are represented in the Degree Matrix ($D$).
    3. **The Graph Laplacian**: Computed as $L = D - A$. This matrix operates on signals over the graph.
    4. **Spectral Analysis**: By solving $Lv = \lambda v$, we extract the eigenvalues (which indicate connectivity) and eigenvectors (which embed the graph geometrically).
    5. **Clustering**: The Fiedler vector ($\lambda_2$) or the first $k$ eigenvectors are used to partition the nodes into communities via sign bisection or $k$-means.
    
    ### Technological Stack
    * **Streamlit & Plotly**: Immersive 3D web interfaces.
    * **NetworkX**: Graph processing.
    * **NumPy / SciPy**: Fast linear algebra matrix decomposition.
    * **scikit-learn**: Geometric $k$-means clustering on the spectral embedding.
    
    *Built for the PES University Linear Algebra Mini-Project.*
    """)
