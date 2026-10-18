
from app.analyzers.file_analyzer import analyze_code

result = analyze_code("main.py")

print("File:", result["file"])
print("Total lines:", result["total_lines"])
print("Empty lines:", result["empty_lines"])
print("Comment lines:", result["comment_lines"])
print("Code lines:", result["code_lines"])
