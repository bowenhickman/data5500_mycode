
import networkx as nx

def count_high_degree_nodes(graph: nx.Graph) -> int:
    """Return the number of nodes with degree greater than 5."""
    return sum(1 for node, degree in graph.degree() if degree > 5)

# Example test
if __name__ == "__main__":
    G = nx.Graph()
    G.add_edges_from([
        (1, 2), (1, 3), (1, 4), (1, 5),
        (1, 6), (1, 7), (2, 3), (3, 4)
    ])
    print("Nodes with degree > 5:", count_high_degree_nodes(G))