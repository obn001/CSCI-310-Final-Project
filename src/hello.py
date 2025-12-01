"""
Monrovia Road Analyzer
A simplified graph-analysis toolkit limited to Monrovia, Liberia.
Author: Olivia Newton
"""

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt


def load_monrovia_graph():
    """Load the drivable road network for Monrovia from OpenStreetMap."""
    print("Loading Monrovia road network... This may take a few seconds.")

    point = ox.geocode("Monrovia, Liberia")

    # Build graph within 10 km
    G = ox.graph_from_point(point, dist=10000, network_type="drive")

    # Edge lengths are already automatically included in new osmnx versions.
    return G


def shortest_route(G, origin, destination):
    orig_node = ox.distance.nearest_nodes(G, origin[1], origin[0])
    dest_node = ox.distance.nearest_nodes(G, destination[1], destination[0])

    route = nx.shortest_path(G, orig_node, dest_node, weight="length")
    distance = nx.shortest_path_length(G, orig_node, dest_node, weight="length")

    return route, distance


def connected_components(G):
    comps = list(nx.connected_components(G.to_undirected()))
    sizes = [len(c) for c in comps]
    return comps, sizes


def centrality_analysis(G, top_n=10):
    print("Computing centrality... This may take a bit.")
    centrality = nx.betweenness_centrality(G, k=500, seed=42)
    ranked = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]


def draw_route(G, route):
    fig, ax = ox.plot_graph_route(G, route, node_size=0)
    plt.show()


def main():
    G = load_monrovia_graph()

    origin = (6.3106, -10.8040)
    destination = (6.3000, -10.7972)

    route, dist = shortest_route(G, origin, destination)
    print(f"Shortest route distance: {dist/1000:.2f} km")
    draw_route(G, route)

    comps, sizes = connected_components(G)
    print(f"Number of connected components: {len(comps)}")
    print(f"Largest component size: {max(sizes)}")

    important_nodes = centrality_analysis(G, top_n=10)
    print("Top 10 most central nodes:")
    for node, score in important_nodes:
        print(f"Node {node}: {score:.5f}")

if __name__ == "__main__":
    main()