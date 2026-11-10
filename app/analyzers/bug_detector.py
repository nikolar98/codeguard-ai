
import ast


def detect_bare_except(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        code = file.read()

    tree = ast.parse(code)
    bugs = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                bugs.append({
                    "line": node.lineno,
                    "type": "bare_except",
                    "message": "Avoid using bare except clauses."
                })

    return bugs

def detect_mutable_defaults(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        code = file.read()

    tree = ast.parse(code)
    bugs = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defaults = node.args.defaults + [
                default
                for default in node.args.kw_defaults
                if default is not None
            ]

            for default in defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    bugs.append({
                        "line": default.lineno,
                        "type": "mutable_default",
                        "message": "Avoid using mutable default arguments."
                    })

    return bugs