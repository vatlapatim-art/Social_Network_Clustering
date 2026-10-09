
import numpy as np
import networkx as nx


def main():
    # Load the built-in social network dataset
    G = nx.karate_club_graph()

    # Convert the graph to an adjacency matrix
    A = nx.to_numpy_array(G, weight=None, dtype=int)

    # Calculate node degrees
    degrees = A.sum(axis=1)

    # Construct the diagonal degree matrix
    D = np.diag(degrees)

    # Display statistics
    print("Dataset: Zachary's Karate Club")
    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())
    print("Adjacency matrix shape:", A.shape)
    print("Degree matrix shape:", D.shape)
    print("Average degree:", round(degrees.mean(), 2))
    print("First 10 node degrees:", degrees[:10])

    print("\nAdjacency matrix (first 5 x 5):")
    print(A[:5, :5])

    print("\nDegree matrix (first 5 x 5):")
    print(D[:5, :5])

    # Save outputs for the other team members
    np.save("adjacency_matrix.npy", A)
    np.save("degree_matrix.npy", D)
    np.save("node_degrees.npy", degrees)

    print("\nSaved adjacency_matrix.npy")
    print("Saved degree_matrix.npy")
    print("Saved node_degrees.npy")


if __name__ == "__main__":
    main()
