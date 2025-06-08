import os

IGNORE = {
    ".venv",
    ".git",
    "__pycache__",
    ".mypy_cache",
    "dist",
    "build",
    ".idea",
    ".vscode",
}

for root, dirs, files in os.walk(".", topdown=True):
    # Filter ignored dirs in-place
    dirs[:] = [d for d in dirs if d not in IGNORE]
    level = root.count(os.sep)
    indent = "  " * level
    print(f"{indent}{os.path.basename(root)}/")
    for f in files:
        if f.endswith(".py"):
            print(f"{indent}  {f}")
