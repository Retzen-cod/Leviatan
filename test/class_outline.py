import os
import ast
import sys
from graphviz import Digraph  # Added import for graph generation
from graphviz.backend.execute import ExecutableNotFound  # Added import

def get_classes(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
        classes = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        bases.append(f"{base.value.id}.{base.attr}" if isinstance(base.value, ast.Name) else base.attr)
                classes[node.name] = bases
        return classes
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return {}

def outline_classes(root_directory):
    classes_map = {}
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_classes = get_classes(file_path)
                if file_classes:
                    classes_map.update(file_classes)
    return classes_map

def generate_graph(classes_map):
    dot = Digraph(comment='Class Diagram')
    for cls, bases in classes_map.items():
        dot.node(cls, cls)
        for base in bases:
            dot.node(base, base)
            dot.edge(base, cls)
    try:
        dot.render('class_diagram', format='png', cleanup=True)
        print("Graph saved to class_diagram.png")
    except ExecutableNotFound:
        print("Error: Graphviz executable not found. Please ensure 'dot' is installed and in your PATH.")

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\otoni\Downloads\Leviatán"
    classes_map = outline_classes(directory)
    for cls, bases in classes_map.items():
        print(f"Clase: {cls} - Hereda de: {bases}")
    print("-" * 40)
    generate_graph(classes_map)
