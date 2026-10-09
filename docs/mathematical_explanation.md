# Mathematical Explanation

## 1. Graphs and Social Networks
- **Concept**: A graph $G = (V, E)$ consists of vertices (nodes) and edges (connections).
- **Purpose**: To mathematically model social networks where nodes are people and edges are friendships.
- **Outcome**: A structural representation of Zachary's Karate Club.

## 2. Adjacency Matrix ($A$)
- **Concept**: An $n \times n$ matrix where $A_{ij} = 1$ if node $i$ is connected to node $j$, and 0 otherwise.
- **Purpose**: To convert the visual graph into a numerical format suitable for linear algebra.
- **Outcome**: A symmetric matrix (for undirected graphs) that captures all direct connections.

## 3. Degree Matrix ($D$)
- **Concept**: A diagonal $n \times n$ matrix where $D_{ii}$ is the degree (number of connections) of node $i$.
- **Purpose**: To quantify the local connectivity (popularity) of each node.
- **Outcome**: A diagonal matrix used to normalize or scale the adjacency matrix.

## 4. Graph Laplacian ($L$)
- **Concept**: Defined as $L = D - A$.
- **Purpose**: To act as a discrete analog to the Laplace operator. It measures how much a node differs from its neighbors.
- **Outcome**: A symmetric, positive semi-definite matrix where row sums equal 0.

## 5. Eigenvalues and Eigenvectors
- **Concept**: Solutions to $Lv = \lambda v$.
- **Purpose**: To find invariant directions (eigenvectors $v$) and their scaling factors (eigenvalues $\lambda$). For the Laplacian, these reveal global network structure.
- **Outcome**: A sorted list of eigenvalues $0 = \lambda_1 \le \lambda_2 \le \dots \le \lambda_n$ and their corresponding eigenvectors.

## 6. Algebraic Connectivity
- **Concept**: The second smallest eigenvalue, $\lambda_2$.
- **Purpose**: To measure how well-connected the graph is. If $\lambda_2 > 0$, the graph is connected.
- **Outcome**: A single scalar value representing network robustness.

## 7. Fiedler Vector
- **Concept**: The eigenvector corresponding to $\lambda_2$.
- **Purpose**: To provide a 1-dimensional embedding of the nodes that optimally preserves graph distances.
- **Outcome**: A vector of length $n$. Nodes with similar values in the Fiedler vector are highly connected.

## 8. Spectral Clustering
- **Concept**: Using the first $k$ eigenvectors (associated with the smallest eigenvalues) to represent the nodes in $k$-dimensional space.
- **Purpose**: To transform the complex graph structure into a geometric space where standard clustering (like k-means) works well.
- **Outcome**: Meaningful community assignments.

## 9. K-Means in Spectral Embedding
- **Concept**: Partitioning the $k$-dimensional rows of the eigenvector matrix into $k$ clusters based on geometric distance.
- **Purpose**: To finalize the community assignments.
- **Outcome**: Discrete labels (0, 1, ..., k-1) for every node.

## 10. Modularity
- **Concept**: A metric that compares the density of edges inside communities to the density expected by chance.
- **Purpose**: To evaluate the quality of the clustering.
- **Outcome**: A score (typically between -0.5 and 1.0). Higher means stronger community structure.
