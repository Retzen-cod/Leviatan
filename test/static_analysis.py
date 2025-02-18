import os
import sys
import re

def analyze_file(file_path):
    total_lines = 0
    comment_lines = 0
    blank_lines = 0
    imports = []  # collect import statements (for Python files)

    ext = os.path.splitext(file_path)[1]
    comment_pattern = None
    # Define patrón de comentarios según extensión
    if ext == '.py':
        comment_pattern = re.compile(r'^\s*#')
    elif ext in ['.js', '.ts', '.java', '.c', '.cpp']:
        comment_pattern = re.compile(r'^\s*//')

    import_pattern = re.compile(r'^\s*(import|from)\s+(\S+)')
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                total_lines += 1
                if not line.strip():
                    blank_lines += 1
                elif comment_pattern and comment_pattern.match(line):
                    comment_lines += 1
                # Extraer imports solo para archivos Python
                if ext == '.py':
                    m = import_pattern.match(line)
                    if m:
                        # For 'from X import ...', take X; for 'import X, Y', split by comma
                        imp = m.group(2).split('.')[0]
                        imports.append(imp)
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
        return None
    return total_lines, comment_lines, blank_lines, list(set(imports))

def analyze_directory(directory):
    report = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            result = analyze_file(file_path)
            if result:
                total, comments, blanks, imports = result
                report[file_path] = {
                    'total_lines': total,
                    'comment_lines': comments,
                    'blank_lines': blanks,
                    'code_lines': total - comments - blanks,
                    'imports': imports
                }
    return report

def generate_dot(report, output_path):
    # Build a mapping: module name -> file path (for Python files only)
    module_map = {}
    for file_path, stats in report.items():
        if file_path.endswith('.py'):
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            module_map[module_name] = file_path

    # Build edges: for each file, if an imported module exists in module_map, create an edge.
    edges = set()
    for file_path, stats in report.items():
        for imp in stats['imports']:
            target = module_map.get(imp)
            if target:
                edges.add((file_path, target))

    lines = []
    lines.append("digraph G {")
    # Create nodes with abbreviated labels (basename)
    for file_path in report:
        label = os.path.basename(file_path)
        lines.append(f'    "{file_path}" [label="{label}"];')
    # Create edges
    for src, dst in edges:
        lines.append(f'    "{src}" -> "{dst}";')
    lines.append("}")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        print(f"DOT file generated: {output_path}")
    except Exception as e:
        print(f"Error writing DOT file: {e}")

# Procesamiento y generación del reporte en formato grafo
directory = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\otoni\Downloads\Leviatán"
report = analyze_directory(directory)
dot_output = os.path.join(r"C:\Users\otoni\Downloads\Leviatán", "test", "static_analysis.dot")
generate_dot(report, dot_output)