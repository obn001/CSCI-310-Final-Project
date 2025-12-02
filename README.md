Monrovia Street Routing Tool

A simple routing application built with OSMnx, NetworkX, and Python that helps users find the shortest route between two streets in Monrovia, Liberia.

            This project includes:

Two different streets distance calculation which also calculate:

Shortest-route calculation

Driving time estimation

Route visualization

VisualStadio Code

                Features

Street Search (if imported in the code) Search for any street name from the loaded Monrovia map.

Shortest Path Calculation – Automatically find the shortest driving route between two streets.

Driving Time Estimate – Calculates an estimated time based on road speeds.

Route Plotting – Visualizes the route on a map using Matplotlib.

Clean Code Structure – Uses functions for loading the graph, searching streets, and generating output.

Technologies Used

Python 3

OSMnx

NetworkX

Matplotlib

Pandas (optional)

Google Colab Notebook (if running online) this was used to test my code and edit it

⚠️ Required dependency: scikit-learn
Install it if you see: ImportError: scikit-learn must be installed…

pip install scikit-learn

Project Structure
/src
   ├── finalproject.py        # Main routing script
   ├── utils.py        # (Optional) helper functions
   └── README.md       # This file

How to Run
Install Dependencies

Run this in your terminal:

pip install osmnx networkx matplotlib scikit-learn

Run the Application
python3 src/finalproject.py

How It Works

Load Monrovia Map

Using OSMnx:

G = ox.graph_from_place("Monrovia, Liberia", network_type="drive")

Convert Street Names → Coordinates

You search the street name inside the street dataset or through OSMnx’s geocoder.

Calculate Shortest Route

Using NetworkX:

route = nx.shortest_path(G, orig_node, dest_node, weight="length")

Estimate Travel Time

Assuming average speed:

time = distance / speed

Plot the Route

Using OSMnx:

ox.plot_graph_route(G, route)

Example Output

Total distance (kilometers)

Estimated time (minutes)

Map showing the route
