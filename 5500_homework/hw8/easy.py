import networkx as nx

def count_nodes(graph: nx.Graph) -> int:
    """Return the number of nodes in a NetworkX graph."""
    return graph.number_of_nodes()

# Example test
if __name__ == "__main__":
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4])
    print("Number of nodes:", count_nodes(G))