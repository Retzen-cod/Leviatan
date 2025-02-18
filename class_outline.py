import inspect
import graphviz
import sys

def get_class_connections(module):
    classes = inspect.getmembers(module, inspect.isclass)
    connections = []
    for name, cls in classes:
        bases = [base.__name__ for base in cls.__bases__]
        for base in bases:
            connections.append((base, name))
    return connections

def generate_class_graph_html(connections, output_file='class_graph'):
    dot = graphviz.Digraph(comment='Class Diagram')
    for base, derived in connections:
        dot.node(base)
        dot.node(derived)
        dot.edge(base, derived)
    try:
        svg = dot.pipe(format='svg').decode('utf-8')
    except graphviz.backend.ExecutableNotFound:
        print("Error: Graphviz executable not found. Please ensure 'dot' is installed and in your PATH.")
        sys.exit(1)
    with open(f"{output_file}.html", "w", encoding="utf-8") as f:
        f.write("<html><body>")
        f.write(svg)
        f.write("</body></html>")

def generate_class_graph_png(connections, output_file='class_graph'):
    dot = graphviz.Digraph(comment='Class Diagram')
    for base, derived in connections:
        dot.node(base)
        dot.node(derived)
        dot.edge(base, derived)
    try:
        png = dot.pipe(format='png')
    except graphviz.backend.ExecutableNotFound:
        print("Error: Graphviz executable not found. Please ensure 'dot' is installed and in your PATH.")
        sys.exit(1)
    with open(f"{output_file}.png", "wb") as f:
        f.write(png)
