
from pathlib import Path

from app.analyzers.file_analyzer import (
    analyze_code,
    detect_structures,
    detect_long_lines,
    detect_long_functions,
    detect_syntax_errors,
    analyze_complexity
)

from app.report_generator import generate_json_report

project_path = Path(".")

total_files = 0
total_lines = 0
report_data = []

for file in project_path.rglob("*.py"):
    if ".venv" in file.parts:
        continue

    result = analyze_code(file)
    result["file"] = str(result["file"])
    long_lines = detect_long_lines(file)
    syntax_error = detect_syntax_errors(file)

    file_report = {
        "file": str(file),
        "statistics": result,
        "syntax_error": syntax_error,
        "long_lines": long_lines
    }

    print("File:", result["file"])
    print("Total lines:", result["total_lines"])
    print("Empty lines:", result["empty_lines"])
    print("Comment lines:", result["comment_lines"])
    print("Code lines:", result["code_lines"])

    if syntax_error is not None:
        print("Syntax Error detected!")
        print("Line:", syntax_error["line"])
        print("Message:", syntax_error["message"])

    else:
        structures = detect_structures(file)
        long_functions = detect_long_functions(file)
        complexity_results = analyze_complexity(file)

        file_report["structures"] = structures
        file_report["long_functions"] = long_functions
        file_report["complexity"] = complexity_results

        print("Functions:", len(structures["functions"]))
        print("Classes:", len(structures["classes"]))
        print("Function names:", structures["functions"])
        print("Class names:", structures["classes"])

        print("Long functions:", len(long_functions))

        for issue in long_functions:
            print(
                f"  Warning: Function '{issue['name']}' "
                f"has {issue['length']} lines "
                f"(starts at line {issue['start_line']})"
            )

        print("Complexity Analysis:")

        for complexity_result in complexity_results:
            print(
                f"  Function '{complexity_result['function']}': "
                f"Complexity {complexity_result['complexity']}"
            )

            if complexity_result["complexity"] > 5:
                print("    Warning: High function complexity!")

    print("Long lines:", len(long_lines))

    for issue in long_lines:
        print(
            f"  Warning: Line {issue['line']} "
            f"has {issue['length']} characters"
        )

    print("---------------------------")

    total_files += 1
    total_lines += result["total_lines"]

    report_data.append(file_report)

print("Total Python files:", total_files)
print("Total project lines:", total_lines)

generate_json_report({
    "total_files": total_files,
    "total_lines": total_lines,
    "files": report_data
})
