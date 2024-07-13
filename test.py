import networkx as nx
import matplotlib.pyplot as plt

# Initialize a directed graph
G = nx.DiGraph()

# Add nodes (you can dynamically add more nodes later)
G.add_node("Node 1", color="blue")
G.add_node("Node 2", color="green")
G.add_node("Node 3", color="red")

# Add edges between nodes
G.add_edge("Node 1", "Node 2")
G.add_edge("Node 2", "Node 3")
G.add_edge("Node 3", "Node 1")

# Get node colors for visualization
node_colors = [G.nodes[node]["color"] for node in G.nodes]

# Draw the graph with matplotlib
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000)
nx.draw_networkx_edges(G, pos, arrows=True)
nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")

# Display the graph
plt.axis("off")
plt.show()
