# Install OSMnx if needed
# %pip install osmnx

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from osmnx.features import features_from_bbox


def load_monrovia_graph():
    """Load the full drivable road network for Monrovia using coordinates."""
    print("Loading Monrovia road network... This may take some time.")

    # Approximate coordinates (Monrovia center)
    monrovia_lat = 6.3000
    monrovia_lon = -10.8000

    # 25 km radius around city center
    dist = 25000
    G = ox.graph_from_point((monrovia_lat, monrovia_lon), dist=dist, network_type="drive")

    # Add bounding box metadata for fast street lookup
    north, south, east, west = ox.utils_geo.bbox_from_point((monrovia_lat, monrovia_lon), dist=dist)
    G.graph['bbox_north'] = north
    G.graph['bbox_south'] = south
    G.graph['bbox_east'] = east
    G.graph['bbox_west'] = west

    print(f"Graph loaded with {len(G.nodes)} nodes and {len(G.edges)} edges.")

    # Add edge speeds + travel times
    G = ox.add_edge_speeds(G)    # uses OSM maxspeed or fallback
    G = ox.add_edge_travel_times(G)

    return G


def get_node_from_street(G, street_name):
    """Find the graph node corresponding to a street name."""
    print(f"\nSearching for street: {street_name}")

    north = G.graph['bbox_north']
    south = G.graph['bbox_south']
    east = G.graph['bbox_east']
    west = G.graph['bbox_west']

    roads = features_from_bbox((north, south, east, west), {"highway": True})

    if "name" not in roads.columns:
        raise ValueError("Road data contains no names.")

    street_roads = roads[roads["name"] == street_name]

    if street_roads.empty:
        print("Street not found. Example available street names:")
        unique_names = roads["name"].dropna().unique()
        for name in unique_names[:20]:
            print(f" - {name}")
        raise ValueError(f"Street '{street_name}' not found.")

    geom = street_roads.iloc[0].geometry

    if hasattr(geom, 'geoms'):  # MultiLineString
        lon, lat = geom.geoms[0].coords[0]
    else:
        lon, lat = geom.coords[0]

    node = ox.distance.nearest_nodes(G, lon, lat)
    print(f"Found node {node} for {street_name}")

    return node


def shortest_route_by_street(G, street1, street2):
    """Compute shortest driving route and travel time between two streets."""
    node1 = get_node_from_street(G, street1)
    node2 = get_node_from_street(G, street2)

    route = nx.shortest_path(G, node1, node2, weight="travel_time")
    distance = nx.shortest_path_length(G, node1, node2, weight="length")
    travel_time = nx.shortest_path_length(G, node1, node2, weight="travel_time")

    return route, distance, travel_time


def draw_route(G, route):
    fig, ax = ox.plot_graph_route(G, route, node_size=0)
    plt.show()


def main():
    G = load_monrovia_graph()

    print("\n==========================")
    print(" Monrovia Route Finder")
    print("==========================")

    """
   Example available street names
  =====================================
 - Popo Beach Junction
 - Small Catholic Junction
 - Turning Point (Junction)
 - Shared Taxi to Paynes ville
 - God's favor woodshop
 - Trans-West African Coastal Highway
 - St. Paul Bridge
 - Hotel Africa Road
 - Kyle Local Road
 - Caldwell Road
 - Mesurado Bridge
 - Benson Street
 - Mechlin Street
 - Horton Avenue
 - Lynch Street
 - McDonald Street
 - Chicken Soup Factory Road
 - Broad Street
 - Clay Street
 - Gurley Street
 - Johnson Street
 - Newport Street
 - Water Street
 - Randall Street
 """
    street1 = input("Enter **starting street**: ")
    street2 = input("Enter **destination street**: ")

    route, dist, time_sec = shortest_route_by_street(G, street1, street2)

    print("\n======= RESULT =======")
    print(f"From: {street1}")
    print(f"To:   {street2}")
    print(f"Shortest Distance: {dist/1000:.2f} km")

    # Convert seconds → minutes
    minutes = time_sec / 60
    print(f"Estimated driving time: {minutes:.1f} minutes\n")

    draw_route(G, route)


if __name__ == "__main__":
    main()
