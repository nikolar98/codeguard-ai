import ast


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



def detect_structures(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        code = file.read()

    tree = ast.parse(code)

    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return {
        "functions": functions,
        "classes": classes
    }



def detect_long_lines(file_name, max_length=79):
    long_lines = []

    with open(file_name, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line_length = len(line.rstrip("\r\n"))

            if line_length > max_length:
                long_lines.append({
                    "line": line_number,
                    "length": line_length
                })

    return long_lines


def detect_long_functions(file_name, max_lines=30):
    with open(file_name, "r", encoding="utf-8") as file:
        code = file.read()

    tree = ast.parse(code)
    long_functions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_length = node.end_lineno - node.lineno + 1

            if function_length > max_lines:
                long_functions.append({
                    "name": node.name,
                    "start_line": node.lineno,
                    "length": function_length
                })

    return long_functions

def detect_syntax_errors(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        code = file.read()

    try:
        ast.parse(code)
        return None

    except SyntaxError as error:
        return {
            "line": error.lineno,
            "message": error.msg
        }
