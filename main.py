from pathlib import Path
from app.analyzers.file_analyzer import analyze_code, detect_structures, detect_long_lines

project_path = Path(".")

total_files = 0
total_lines = 0

for file in project_path.rglob("*.py"):
    if ".venv" in file.parts:
        continue

    result = analyze_code(file)
    structures = detect_structures(file)
    long_lines = detect_long_lines(file)

    print("File:", result["file"])
    print("Total lines:", result["total_lines"])
    print("Empty lines:", result["empty_lines"])
    print("Comment lines:", result["comment_lines"])
    print("Code lines:", result["code_lines"])
    print("Functions:", len(structures["functions"]))
    print("Classes:", len(structures["classes"]))
    print("Long lines:", len(long_lines))

    for issue in long_lines:
        print(f"  Warning: Line {issue['line']} has {issue['length']} characters")

    print("---------------------------")

    total_files += 1
    total_lines += result["total_lines"]

print("Total Python files:", total_files)
print("Total project lines:", total_lines)
