# User Guide

## Introduction
This application allows you to explore the math behind Social Network Community Detection.

## Navigation
1. **Dataset Selection**: On the left sidebar, choose Zachary's Karate Club (default) or upload a CSV edge list.
2. **Cluster Settings**: Use the slider to choose the number of communities (2, 3, or 4). Change the random seed if you want to see if k-means results vary.
3. **Overview**: See basic graph metrics (Nodes, Edges, Average Degree).
4. **Network Visualization**: Compare the original graph layout with the color-coded community graph.
5. **Matrix Representations**: Use the tabs to view the Adjacency (A), Degree (D), and Laplacian (L) matrices as heatmaps.
6. **Eigenvalue Analysis**: View the plot of the smallest eigenvalues. Notice the gap after the 0 eigenvalue. Expand the "View Fiedler Vector" box to see numerical values.
7. **Node Inspection**: Select a specific node (e.g., node 0 or node 33 in the Karate Club) to see its degree and community.
8. **Downloads**: Export your results for your report.

## Uploading a CSV
If you upload a CSV, ensure it has at least two columns. The first column is the source node, and the second is the target node. Headers are required but the names don't matter (e.g., `source`, `target`).
