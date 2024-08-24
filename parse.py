import argparse
import json
import pathlib
from collections import defaultdict
import sys
import os

def find_files(directory):
    """Find all .cc and .h files in the directory."""
    path = pathlib.Path(directory)
    return set([file for file in path.glob("**/*.cc")] + [file for file in path.glob("**/*.h")])

def parse_file(file_path, dir):
    """Parse a file to find its import relationships and return a list of pathlib.Path objects."""
    imports = set()
    file_dir = file_path.parent
    
    with open(file_path, 'r') as f:
        for line in f:
            # Simple heuristic: looking for #include directives
            if line.startswith('#include') and '<' not in line:
                parts = line.split()
                if len(parts) > 1:
                    include_path = parts[1].strip('\"')
                    # Create a pathlib.Path object relative to the directory of the current file
                    if os.path.exists(str(file_dir / include_path)):
                        import_path = file_dir / include_path
                        imports.add(import_path)
                    else:
                        import_path = dir / include_path
                        imports.add(import_path)
    
    return list(imports)

def generate_graph(files, dirstring):
    """Generate nodes and links from file import relationships."""
    dir = pathlib.Path(dirstring)
    nodes = []
    links = []
    for file in files:
        file_type = 0
        if "main" in str(file):
            file_type = 1
        elif "srsenb" in str(file):
            file_type = 2
        elif "srsepc" in str(file):
            file_type = 3
        elif "srsue" in str(file):
            file_type = 4
        else:
            file_type = 5
        nodes.append({'id': str(file), 'group': file_type})
        imports = parse_file(file, dir)
        for imp in imports:
            if imp in files:
                links.append({'source': str(file), 'target': str(imp), 'value': 2})
    
    return nodes, links

def parse():
    parser = argparse.ArgumentParser(description='Generate JSON for file import relationships.')
    parser.add_argument('directory', type=str, help='Directory to scan for .cc and .h files')
    return parser.parse_args()


def main():
    args = parse()

    files = find_files(args.directory)
    nodes, links = generate_graph(files, args.directory)

    graph = {'nodes': nodes, 'links': links}

    output_file = pathlib.Path(args.directory) / 'graph.json'
    with open(output_file, 'w') as f:
        json.dump(graph, f, indent=4)

    print(f'Graph data has been written to {output_file}')
    return 0

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
