import argparse
import json
import pathlib
from collections import defaultdict
import sys
import os
import uuid

def find_files(directory):
    """Find all .cc and .h files in the directory."""
    path = pathlib.Path(directory)
    return set([file for file in path.glob("**/*.cc")] + [file for file in path.glob("**/*.h")])

def parse_file_imports(file_path, dir):
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

def parse_file_declarations(file_path):
    functions = set()
    
    with open(file_path, 'r') as f:
        for line in f:
            if "if" in line or "for" in line or "while" in line:
                continue
            if '(' in line and '::' in line:
                parts = line.split('(')
                if len(parts) > 1:
                    functions.add(parts[0].strip())
    
    return list(functions)

def parse_file_calls(file_path):
    functions = []
    func_stack = []
    
    with open(file_path, 'r') as f:
        for line in f:
            if "if" in line or "for" in line or "while" in line:
                continue
            if '(' in line and '::' in line:
                func_stack.append(line.split("(")[0].strip())
            if '}' in line:
                func_stack = []

            if '(' in line and '::' not in line:
                parts = line.split('(')
                if len(parts) > 0 and len(func_stack) > 0:
                    functions.append({ "to": parts[0].strip().split(" ")[-1].split("::")[-1].split(".")[-1].split(">")[-1], "from": func_stack[0].strip().split(" ")[-1].split("::")[-1].split(".")[-1].split(">")[-1]})
    
    return functions





def generate_file_graph(files, dirstring):
    """Generate nodes and links from file import relationships."""
    dir = pathlib.Path(dirstring)
    nodes = []
    links = []
    for file in files:
        file_type = ""
        if "main" in str(file):
            file_type = "Main"
        elif "srsenb" in str(file):
            file_type = "srsRAN eNB"
        elif "srsepc" in str(file):
            file_type = "srsRAN EPC"
        elif "srsue" in str(file):
            file_type = "srsRAN UE"
        else:
            file_type = "Common"
        current_uuid = str(uuid.uuid4())
        nodes.append({'id': current_uuid, "user": str(file), 'description': file_type})
    for node in nodes:
        imports = parse_file_imports(pathlib.Path(node["user"]), dir)
        for imp in imports:
            matching_nodes = [item for item in nodes if str(imp) in item["user"]]
            if len(matching_nodes) > 0:
                links.append({'source': node["id"], 'target': matching_nodes[0]["id"], 'value': 2})
    
    return nodes, links

def generate_function_graph(files):
    """Generate nodes and links from file import relationships."""
    nodes = []
    links = []
    name_to_id = {}
    for file in files:
        functions = parse_file_declarations(file)
        for func in functions:
            current_uuid = str(uuid.uuid4())
            func_name = func.split(" ")[-1].split("::")[-1].split(".")[-1].split(">")[-1]
            func_desc = func.split(" ")[-1].split("::")[0]
            if func_desc == func_name or "~" in func_name or "." in func_desc or ">" in func_desc:
                continue
            if func_name == "" or func_desc == "":
                continue
            if  func_name not in name_to_id.keys():
                nodes.append({'id': current_uuid, "user": func_name, 'description': func_desc})
            name_to_id[func.split(" ")[-1].split("::")[-1]] = current_uuid

    for file in files:
        functions = parse_file_calls(file)
        for func in functions:
            if func["to"] in name_to_id.keys() and func["from"] in name_to_id.keys():
                links.append({'source': name_to_id[func["from"]], 'target': name_to_id[func["to"]],'value': 2})


    
    return nodes, links



def parse():
    parser = argparse.ArgumentParser(description='Generate JSON for file import relationships.')
    parser.add_argument('directory', type=str, help='Directory to scan for .cc and .h files')
    parser.add_argument('--output', type=str, help='output file name')
    parser.add_argument('--type', type=str, help='output file name')
    return parser.parse_args()


def main():
    args = parse()

    nodes = []
    links = []

    files = find_files(args.directory)
    if args.type == "files":
        nodes, links = generate_file_graph(files, ".")
    elif args.type == "functions":
        nodes, links = generate_function_graph(files)
    graph = {'nodes': nodes, 'links': links}

    output_file = pathlib.Path(args.output)
    print(f"Found {len(nodes)} nodes")
    print(f"Generated {len(links)} links")
    with open(output_file, 'w') as f:
        json.dump(graph, f, indent=4)

    print(f'Graph data has been written to {output_file}')
    return 0

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
