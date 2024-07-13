import sys
import os
import mimetypes
import networkx as nx
import matplotlib.pyplot as plt




# Display the graph


def is_text_file(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type and mime_type.startswith('text')


def walk_directory(path, tabs=""):
    global G
    global module_set
    print(f"{tabs}entering directory: ", path)
    for file in os.listdir(path):
        if(os.path.isdir(os.path.join(path, file))):
            walk_directory(os.path.join(path, file), tabs+"\t")
        elif is_text_file(os.path.join(path, file)):
            print(f"{tabs}-" + os.path.join(path, file))
            file_module = '/'.join(os.path.join(path, file).split('/')[1:])
            if not file_module in module_set:
                G.add_node(file_module, color='green')
                module_set.add(file_module)
            try:
                with open(os.path.join(path, file), 'r') as f:
                    for line in f.readlines()[:50]:
                        if '#include \"' in line:
                            module_name = line.split('\"')[1]
                            if not module_set in module_set:
                                G.add_node(module_name, color="green")
                                module_set.add(module_name)
                            G.add_edge(module_name, file_module)


            except UnicodeDecodeError as e:
                print(f"{tabs}Failed to parse binary file")

def main():
    path = sys.argv[1]

    global G
    global module_set

    module_set = set()

    G = nx.DiGraph()

    G.add_node("Node 1", color="blue")
    G.add_node("Node 2", color="green")
    G.add_node("Node 3", color="red")

    G.add_edge("Node 1", "Node 2")
    G.add_edge("Node 2", "Node 3")
    G.add_edge("Node 3", "Node 1")
    walk_directory(path)
    pos = nx.spring_layout(G)  # positions for all nodes
    node_colors = [G.nodes[node]["color"] for node in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=10)
    nx.draw_networkx_edges(G, pos, arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=5, font_family="sans-serif")

    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
    print("FINISED!")
