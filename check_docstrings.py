"""Report modules, classes and functions that lack a docstring."""
import ast
import sys
from pathlib import Path


def check_file(path):
    """Return a list of names in `path` that have no docstring."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    missing = []
    if ast.get_docstring(tree) is None:
        missing.append("module")
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if ast.get_docstring(node) is None:
                missing.append(f"{node.name} (line {node.lineno})")
    return missing


if __name__ == "__main__":
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    for file in sorted(folder.rglob("*.py")):
        if ".venv" in file.parts:
            continue
        for name in check_file(file):
            print(f"{file}: missing docstring -> {name}")