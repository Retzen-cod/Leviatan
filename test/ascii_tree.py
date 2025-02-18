import os
import sys

def generate_ascii_tree(start_path, prefix=""):
    tree_lines = []
    entries = sorted(os.listdir(start_path))
    entries_count = len(entries)
    for idx, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        connector = "└──" if idx == entries_count - 1 else "├──"
        tree_lines.append(f"{prefix}{connector} {entry}")
        if os.path.isdir(path):
            extension = "    " if idx == entries_count - 1 else "│   "
            tree_lines.extend(generate_ascii_tree(path, prefix + extension))
    return tree_lines

# Ejecución directa sin main
start_dir = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\otoni\Downloads\Leviatán"
# Agrega la carpeta raíz a la salida
root_name = os.path.basename(os.path.normpath(start_dir))
output = [root_name]
output.extend(generate_ascii_tree(start_dir))
tree_text = "\n".join(output)
print(tree_text)
with open("tree_structure.txt", "w", encoding="utf-8") as f:
    f.write(tree_text)
