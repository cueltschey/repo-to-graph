import sys
import os
import mimetypes
import networkx as nx
import matplotlib.pyplot as plt

# Initialize a directed graph

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


def is_text_file(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type and mime_type.startswith('text')


def walk_directory(path, tabs=""):
    print(f"{tabs}entering directory: ", path)
    for file in os.listdir(path):
        if(os.path.isdir(os.path.join(path, file))):
            walk_directory(os.path.join(path, file), tabs+"\t")
        elif is_text_file(os.path.join(path, file)):
            print(f"{tabs}-" + file)
            try:
                with open(os.path.join(path, file), 'r') as f:
                    print(f.readlines())
            except UnicodeDecodeError as e:
                print(f"{tabs}Failed to parse binary file")

def main():
    path = sys.argv[1]

    G = nx.DiGraph()
    walk_directory(path)
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
    print("FINISED!")
