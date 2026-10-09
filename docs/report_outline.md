# Mini-Project Report Outline

## 1. Title Page
- **Project Title**: Social Network Community Detection using Spectral Clustering
- **Course**: Linear Algebra (UE25MA242A)
- **Team Members**: [Names and SRNs]
- **Instructor**: [Faculty Name]
- **Date**: [Submission Date]

## 2. Abstract
A brief summary of the project: applying eigenvalue and eigenvector analysis to graph Laplacians for identifying communities in Zachary's Karate Club dataset.

## 3. Introduction
- Background on social networks and graph theory.
- The importance of community detection.
- Motivation for using linear algebra.

## 4. Problem Statement
**Problem 13**: "Social Networks, Clustering, and Eigenvalue Problems"
Objective: To mathematically model a social network and implement spectral clustering to divide the network into distinct communities.

## 5. Mathematical Formulation
- Definition of $G = (V, E)$
- Construction of Adjacency Matrix $A$ and Degree Matrix $D$
- Formulation of Graph Laplacian $L = D - A$
- The Eigenvalue Equation $Lv = \lambda v$
- Properties of Algebraic Connectivity ($\lambda_2$) and the Fiedler Vector.

## 6. System Architecture and Implementation
- **Tools**: Python, NumPy, SciPy, NetworkX, Streamlit.
- **Modules**:
  - Data loading
  - Matrix generation
  - Laplacian computation
  - Spectral clustering (k-means)
  - Visualization and UI

## 7. Results and Analysis
- **Dataset**: Zachary's Karate Club (34 nodes, 78 edges).
- **Matrix properties verified**: Symmetry, diagonal degree, row sum to 0.
- **Eigenvalue spectrum**: Show smallest eigenvalues.
- **Detected Communities**: Compare k=2 vs k=4.
- **Modularity**: Report modularity scores for the clusters.

## 8. Testing and Validation
- Unit tests written with `pytest`.
- Verification of zero eigenvalues for disconnected graphs.
- Eigenvalue residual checks.

## 9. Limitations
- Matrix operations ($O(n^3)$) scale poorly for massive graphs without sparse matrix methods.
- K-Means can be sensitive to initialization if seed is not fixed.

## 10. Conclusion
Spectral clustering effectively utilizes the global structure captured by the Laplacian's eigenvectors to find communities, demonstrating a powerful real-world application of Linear Algebra.

## 11. References
1. Zemlyanova, A. "Applied Projects for an Introductory Linear Algebra Class".
2. PES University Guidelines: UE25MA242A_MFAD - Mini-Project Guidelines.
3. Zachary, W. W. (1977). An Information Flow Model for Conflict and Fission in Small Groups.
