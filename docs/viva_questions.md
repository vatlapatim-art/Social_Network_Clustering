# Viva Questions and Answers

1. **What is a graph in the context of this project?**
   A mathematical structure consisting of nodes (people) and edges (relationships).
2. **What is an Adjacency Matrix ($A$)?**
   A square matrix where $A_{ij} = 1$ if an edge exists between node $i$ and node $j$, and 0 otherwise.
3. **Why is the Adjacency Matrix symmetric for this project?**
   Because the social network is undirected (friendships are mutual).
4. **What is a Degree Matrix ($D$)?**
   A diagonal matrix where the $i$-th entry on the diagonal represents the number of edges connected to node $i$.
5. **How is the Graph Laplacian calculated?**
   $L = D - A$.
6. **What is the significance of the row sums in the Laplacian?**
   They always sum to 0 because the degree of a node equals the number of 1s in its row in the adjacency matrix.
7. **What is an eigenvalue and eigenvector?**
   For a matrix $L$, a scalar $\lambda$ and vector $v$ such that $Lv = \lambda v$.
8. **Why does the Laplacian always have an eigenvalue of 0?**
   Because the vector of all 1s is an eigenvector: $L \cdot \vec{1} = (D - A) \vec{1} = \vec{0} = 0 \cdot \vec{1}$.
9. **What does the multiplicity of the zero eigenvalue tell us?**
   It equals the number of connected components in the graph.
10. **What is Algebraic Connectivity?**
    The second smallest eigenvalue of the Laplacian ($\lambda_2$). It measures how well-connected the graph is.
11. **What is the Fiedler vector?**
    The eigenvector corresponding to the algebraic connectivity ($\lambda_2$).
12. **How does the Fiedler vector help in community detection?**
    The signs (positive/negative) or values of the Fiedler vector can partition the graph into two communities with minimal edge cuts.
13. **What is Spectral Clustering?**
    A clustering technique that uses the eigenvectors of the Laplacian matrix to embed data into a lower-dimensional space before applying a standard clustering algorithm like K-Means.
14. **Why not just apply K-Means directly to the Adjacency Matrix?**
    The adjacency matrix rows are sparse and don't cleanly represent global community structure, whereas eigenvectors capture global connectivity and form continuous clusters.
15. **What is Modularity?**
    A metric that measures the density of edges within communities compared to the density of edges between communities.
16. **Why do we use Zachary's Karate Club dataset?**
    It's a standard benchmark dataset in network science where the true community split (arising from a conflict between the administrator and instructor) is known.
17. **What happens if a graph is disconnected?**
    $\lambda_2$ becomes 0, and the Fiedler vector approach needs to be adapted or applied to each component separately.
18. **Is the Graph Laplacian positive semi-definite?**
    Yes, which means all its eigenvalues are non-negative ($\lambda_i \ge 0$).
19. **What is the numerical tolerance mentioned in the eigenvalue analysis?**
    Floating-point math can result in a 0 eigenvalue being calculated as `1e-15`. We use a tolerance (e.g., `< 1e-10`) to treat these as mathematical zeros.
20. **How is the normalized Laplacian different from the combinatorial one?**
    The normalized Laplacian scales the matrix by the node degrees, making the diagonal entries 1. It is often preferred for graphs with highly variable node degrees.
21. **What is the K-Means algorithm?**
    An algorithm that groups data points into $K$ clusters by minimizing the variance within each cluster.
22. **Why does the spectral bisection method use a sign threshold (e.g., $\ge 0$)?**
    Because the Fiedler vector embeds nodes on a 1D line centered around 0. Nodes $>0$ are highly connected to each other, as are nodes $<0$.
23. **What does the Adjusted Rand Index (ARI) measure?**
    It measures the similarity between two sets of data clusterings, adjusted for chance. 1.0 is a perfect match.
24. **How do you ensure reproducibility in your clustering?**
    By passing a fixed `random_seed` to the K-Means algorithm and the graph layout generator.
25. **What is the runtime complexity of computing eigenvalues?**
    For an $n \times n$ dense matrix, it is typically $O(n^3)$, which is why spectral clustering can be slow for massive networks without sparse approximations.
