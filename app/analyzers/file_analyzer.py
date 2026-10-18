
def analyze_code(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        code = file.readlines()

    total_lines = len(code)
    empty_lines = 0
    comment_lines = 0
    code_lines = 0

    for line in code:
        if line.strip() == "":
            empty_lines += 1
        elif line.strip().startswith("#"):
            comment_lines += 1
        else:
            code_lines += 1

    return {
        "file": file_name,
        "total_lines": total_lines,
        "empty_lines": empty_lines,
        "comment_lines": comment_lines,
        "code_lines": code_lines
    }
