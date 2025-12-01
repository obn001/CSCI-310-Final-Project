#%pip install osmnx
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from osmnx.features import features_from_bbox # Import features_from_bbox directly


def load_monrovia_graph():
    """Load the full drivable road network for Monrovia using coordinates."""
    print("Loading Monrovia road network... This may take some time.")
    # Approximate coordinates for Monrovia, Liberia (e.g., city center)
    monrovia_lat = 6.3000
    monrovia_lon = -10.8000  # West longitude is negative
    # Define a distance in meters around the point to include in the graph
    dist = 15000  # e.g., 15 km radius
    G = ox.graph_from_point((monrovia_lat, monrovia_lon), dist=dist, network_type="drive")

    # Explicitly calculate and add bounding box to graph metadata for ox.geometries_from_bbox
    north, south, east, west = ox.utils_geo.bbox_from_point((monrovia_lat, monrovia_lon), dist=dist)
    G.graph['bbox_north'] = north
    G.graph['bbox_south'] = south
    G.graph['bbox_east'] = east
    G.graph['bbox_west'] = west

    print(f"Graph loaded with {len(G.nodes)} nodes and {len(G.edges)} edges.")
    return G


def get_node_from_street(G, street_name):
    """
    Given a street name, find a node on that street.
    Looks up OSM geometries within the graph's bounding box,
    picks the first coordinate, and finds nearest node.
    """
    print(f"Searching for street: {street_name}")

    # Get the bounding box of the graph G to query geometries within this area
    north = G.graph['bbox_north']
    south = G.graph['bbox_south']
    east = G.graph['bbox_east']
    west = G.graph['bbox_west']

    # Get all road geometries within the graph's bounding box using features_from_bbox
    roads = features_from_bbox((north, south, east, west), {"highway": True})

    # Filter to only the street we want
    street_roads = roads[roads["name"] == street_name]

    if street_roads.empty:
        raise ValueError(f"Street '{street_name}' not found within the graph's area.")

    # Take the first geometry for this street
    geom = street_roads.iloc[0].geometry

    # Handle potentially multi-part geometries (e.g., MultiLineString)
    if hasattr(geom, 'geoms'):
        # If it's a multi-part geometry, take the first coordinate of the first part
        lon, lat = geom.geoms[0].coords[0]
    else:
        # If it's a single-part geometry, take its first coordinate
        lon, lat = geom.coords[0]

    # Convert street coordinate to graph node
    node = ox.distance.nearest_nodes(G, lon, lat)

    print(f"Found node {node} for {street_name}")
    return node


def shortest_route_by_street(G, street1, street2):
    """
    Compute shortest driving route between two streets.
    """
    node1 = get_node_from_street(G, street1)
    node2 = get_node_from_street(G, street2)

    route = nx.shortest_path(G, node1, node2, weight="length")
    distance = nx.shortest_path_length(G, node1, node2, weight="length")

    return route, distance


def draw_route(G, route):
    """
    Draw the route on a map.
    """
    fig, ax = ox.plot_graph_route(G, route, node_size=0)
    plt.show()


def main():
    # Load road network
    G = load_monrovia_graph()

    # Streets for analysis
    street1 = "Tubman Boulevard"
    street2 = "Nelson Street"

    # Calculate route
    route, dist = shortest_route_by_street(G, street1, street2)

    print(f"\nShortest driving distance from {street1} to {street2}:")
    print(f"{dist/1000:.2f} km\n")

    # Visualize
    draw_route(G, route)


if __name__ == "__main__":
    main()