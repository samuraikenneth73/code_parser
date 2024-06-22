import os
import ast


def get_python_files(directory):
    """Recursively get all Python files in the given directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def extract_imports(file_path):
    """Extract import statements from a given Python file."""
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # imports.append(alias.name.split(".")[0])  # Handle base import name
                imports.append(alias.name)  # Handle base import name
        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                # imports.append(node.module.split(".")[0])  # Handle base import name
                imports.append(node.module)  # Handle base import name

    return imports


def build_import_relationships(codebase_path):
    """Build relationships of imports within the codebase."""
    python_files = get_python_files(codebase_path)
    import_map = {file: [] for file in python_files}
    reverse_import_map = {file: [] for file in python_files}

    # Populate the import map
    for file in python_files:
        imports = extract_imports(file)
        import_map[file] = imports

    # Populate the reverse import map
    for file, imports in import_map.items():
        for imp in imports:
            for other_file in python_files:
                if imp.split(".")[0] in other_file or other_file.endswith(
                    f"{imp.replace('.', '\\')}.py"
                ):
                    print("here")
                    reverse_import_map[other_file].append(file)

    return import_map, reverse_import_map


def get_imports_for_file(file_path, import_map):
    """Get all files that the given file imports."""
    return import_map.get(file_path, [])


def get_usage_of_file(file_path, reverse_import_map):
    """Get all files that use the given file."""
    return reverse_import_map.get(file_path, [])


if __name__ == "__main__":
    codebase_path = "<path to your codebase>"
    import_map, reverse_import_map = build_import_relationships(codebase_path)
    file_to_check = "<path to file to check>"
    imports = get_imports_for_file(file_to_check, import_map)
    usages = get_usage_of_file(file_to_check, reverse_import_map)

    print(f"Files imported by {file_to_check}: {imports}")
    print(f"Files using {file_to_check}: {usages}")
