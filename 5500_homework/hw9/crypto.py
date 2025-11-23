"""
hw9_crypto_arbitrage.py

Searches for cryptocurrency arbitrage opportunities using a directed graph.

- Fetches live exchange rates from the CoinGecko API for 7 top coins
- Builds a directed weighted graph with NetworkX
- Finds all simple paths between every ordered pair of coins
- For each path, computes:
    * forward path weight
    * reverse path weight (using the reversed path, if it exists)
    * factor = forward_weight * reverse_weight
- Reports all path details
- Tracks:
    * smallest factor and its paths (best negative arbitrage)
    * greatest factor and its paths (best positive arbitrage)
    * best (maximum) forward path per ordered currency pair
"""

import requests  # used to call the CoinGecko HTTP API
import networkx as nx  # used to build and analyze a directed graph


# Base URL for the CoinGecko simple price API
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

# Mapping from CoinGecko "id" (full coin name) to shorter ticker symbol
# These ticker symbols will be used as node names in the graph
ID_TO_TICKER = {
    "ethereum": "eth",
    "bitcoin": "btc",
    "litecoin": "ltc",
    "ripple": "xrp",
    "cardano": "ada",
    "bitcoin-cash": "bch",
    "eos": "eos",
}

# Build the comma-separated list of ids for the API query
IDS = ",".join(ID_TO_TICKER.keys())

# Build the comma-separated list of vs_currencies for the API query
VS_CURRENCIES = "eth,btc,ltc,xrp,ada,bch,eos"


def fetch_prices():
    """
    Fetch the most recent exchange rates for the chosen coins from CoinGecko.

    Returns:
        dict: Parsed JSON data where keys are coin ids and values are dicts
              mapping ticker symbols to exchange rates.
    """
    # Build the URL query parameters for the HTTP request
    params = {
        "ids": IDS,
        "vs_currencies": VS_CURRENCIES,
    }

    # Send an HTTP GET request to the CoinGecko API with a timeout for safety
    response = requests.get(COINGECKO_URL, params=params, timeout=10)

    # Raise an exception if the HTTP request failed (non-2xx status code)
    response.raise_for_status()

    # Parse and return the JSON response as a Python dictionary
    return response.json()


def build_graph(price_data):
    """
    Build a directed weighted graph from the CoinGecko price data.

    Nodes are ticker symbols (for example: 'btc', 'eth', etc.).
    Edges are directed exchange rates with attribute 'weight' equal to the rate.

    Args:
        price_data (dict): JSON dictionary returned by fetch_prices().

    Returns:
        networkx.DiGraph: Directed graph with weighted edges.
    """
    # Create an empty directed graph
    graph = nx.DiGraph()

    # Loop over every coin id (for example 'ethereum') and its quotes dictionary
    for coin_id, quotes in price_data.items():
        # Convert the full coin id to its shorter ticker (for example 'eth')
        from_ticker = ID_TO_TICKER[coin_id]

        # Make sure the ticker node exists in the graph
        graph.add_node(from_ticker)

        # Loop over every quoted target ticker and its exchange rate
        for to_ticker, rate in quotes.items():
            # Skip this entry if the rate is missing (None)
            if rate is None:
                continue

            # Add a directed edge from the source ticker to the target ticker
            # The edge attribute 'weight' stores the numeric exchange rate
            graph.add_edge(from_ticker, to_ticker, weight=float(rate))

    # Return the finished directed graph
    return graph


def compute_path_weight(graph, path):
    """
    Compute the weight of a path by multiplying the weights of all edges.

    If any edge in the path does not exist in the directed graph, return None.

    Args:
        graph (nx.DiGraph): Graph containing the nodes and edges.
        path (list[str]): List of node names in order, e.g. ['btc', 'xrp', 'eth'].

    Returns:
        float or None: Product of edge weights along the path, or None if invalid.
    """
    # Start the product at 1.0 so multiplication works correctly
    weight_product = 1.0

    # Loop over consecutive node pairs (u -> v) in the path
    for i in range(len(path) - 1):
        # Current node in the path
        u = path[i]
        # Next node in the path
        v = path[i + 1]

        # If there is no directed edge from u to v, the path is invalid
        if not graph.has_edge(u, v):
            return None

        # Read the edge weight (exchange rate) from u to v
        edge_weight = graph[u][v].get("weight")

        # If the edge has no weight attribute, treat the path as invalid
        if edge_weight is None:
            return None

        # Multiply this edge weight into the running product
        weight_product *= edge_weight

    # Return the final product of all edge weights along the path
    return weight_product


def main():
    """
    Main function that:
    - fetches prices
    - builds the graph
    - scans all paths between all ordered currency pairs
    - prints every path with forward and reverse weights and factor
    - tracks smallest and greatest factors across the entire graph
    - tracks and prints the best forward path for each currency pair
    """
    # Print a simple status message before calling the API
    print("Fetching latest prices from CoinGecko...")

    # Call the API and store the price data dictionary
    price_data = fetch_prices()

    # Build the directed weighted graph from the price data
    graph = build_graph(price_data)

    # Print the list of graph nodes (currency tickers)
    print("Graph nodes (currencies):")
    print(list(graph.nodes))

    # Print the total number of nodes in the graph
    print("\nNumber of nodes:", graph.number_of_nodes())

    # Print the total number of edges in the graph
    print("Number of edges:", graph.number_of_edges(), "\n")

    # Get a simple list of all ticker nodes in the graph
    tickers = list(graph.nodes)

    # Initialize the smallest arbitrage factor across all paths to None
    smallest_factor = None
    # Initialize the forward path associated with the smallest factor
    smallest_forward_path = None
    # Initialize the reverse path associated with the smallest factor
    smallest_reverse_path = None

    # Initialize the greatest arbitrage factor across all paths to None
    greatest_factor = None
    # Initialize the forward path associated with the greatest factor
    greatest_forward_path = None
    # Initialize the reverse path associated with the greatest factor
    greatest_reverse_path = None

    # Loop over every ordered pair of distinct source and target tickers
    for source in tickers:
        for target in tickers:
            # Skip cases where the source and target are the same currency
            if source == target:
                continue

            # Print a header for this specific source-to-target currency pair
            print(f"Paths from {source} to {target}")

            # Use NetworkX to get every simple path from source to target
            all_paths = list(nx.all_simple_paths(graph, source=source, target=target))

            # If there are no paths at all for this pair, print a message and move on
            if not all_paths:
                print(f"No paths found from {source} to {target}\n")
                continue

            # Initialize the best forward path weight for this specific pair to None
            best_forward_weight = None
            # Initialize the best forward path itself for this pair to None
            best_forward_path = None

            # Loop over every simple path returned by NetworkX
            for forward_path in all_paths:
                # Compute the forward path weight (source to target)
                forward_weight = compute_path_weight(graph, forward_path)

                # If the forward path is invalid, skip it
                if forward_weight is None:
                    continue

                # If this is the first valid path or has a larger forward weight,
                # update the best forward path for this currency pair
                if best_forward_weight is None or forward_weight > best_forward_weight:
                    best_forward_weight = forward_weight
                    best_forward_path = forward_path

                # Build the reverse path by reversing the node order
                reverse_path = list(reversed(forward_path))

                # Compute the reverse path weight (target back to source)
                reverse_weight = compute_path_weight(graph, reverse_path)

                # If the reverse path is invalid, skip the arbitrage factor calculation
                if reverse_weight is None:
                    continue

                # Compute the arbitrage factor as forward_weight * reverse_weight
                factor = forward_weight * reverse_weight

                # Print the forward path and its weight
                print("  forward path:", forward_path, "weight:", forward_weight)

                # Print the reverse path and its weight
                print("  reverse path:", reverse_path, "weight:", reverse_weight)

                # Print the product of the forward and reverse path weights
                print("  factor:", factor, "\n")

                # Update the smallest factor across the entire graph if needed
                if smallest_factor is None or factor < smallest_factor:
                    smallest_factor = factor
                    smallest_forward_path = forward_path
                    smallest_reverse_path = reverse_path

                # Update the greatest factor across the entire graph if needed
                if greatest_factor is None or factor > greatest_factor:
                    greatest_factor = factor
                    greatest_forward_path = forward_path
                    greatest_reverse_path = reverse_path

            # After processing all paths for this source-target pair,
            # print the best forward path (the one with the largest forward_weight)
            if best_forward_path is not None:
                print(
                    "  Best forward path from",
                    source,
                    "to",
                    target,
                    "gives",
                    best_forward_weight,
                    target,
                    "for 1",
                    source,
                )
            else:
                # This branch should rarely happen because we already checked all_paths,
                # but keep it for completeness.
                print("  No valid forward paths found that could be evaluated.")

            # Print a blank line to separate this pair from the next one
            print()

    # After all currency pairs have been processed, print a summary header
    print("Summary of arbitrage factors")

    # If a smallest factor was found, print it and its associated paths
    if smallest_factor is not None:
        print("Smallest paths weight factor:", smallest_factor)
        print("Forward path:", smallest_forward_path)
        print("Reverse path:", smallest_reverse_path)
        print()

    # If a greatest factor was found, print it and its associated paths
    if greatest_factor is not None:
        print("Greatest paths weight factor:", greatest_factor)
        print("Forward path:", greatest_forward_path)
        print("Reverse path:", greatest_reverse_path)


# Only run the main function when this file is executed directly
if __name__ == "__main__":
    main()

