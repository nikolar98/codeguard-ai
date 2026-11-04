from app.analyzers.file_analyzer import (
    analyze_code,
    detect_syntax_errors,
    detect_long_lines,
    analyze_complexity,
    detect_structures,
    detect_long_functions
)


def test_detect_syntax_errors(tmp_path):
    test_file = tmp_path / "example.py"

    test_file.write_text(
        "def calculate(a, b)\n"
        "    return a + b\n",
        encoding="utf-8"
    )

    result = detect_syntax_errors(test_file)

    assert result is not None
    assert result["line"] == 1
    assert "expected ':'" in result["message"]


def test_analyze_code(tmp_path):
    test_file = tmp_path / "example.py"

    test_file.write_text(
        "# Comment\n"
        "\n"
        "x = 10\n"
        "y = 20\n",
        encoding="utf-8"
    )

    result = analyze_code(test_file)

    assert result["total_lines"] == 4
    assert result["empty_lines"] == 1
    assert result["comment_lines"] == 1
    assert result["code_lines"] == 2


def test_detect_long_lines(tmp_path):
    test_file = tmp_path / "example.py"

    test_file.write_text(
        "x = 10\n"
        "message = 'This is a long line'\n",
        encoding="utf-8"
    )

    result = detect_long_lines(test_file, max_length=20)

    assert len(result) == 1
    assert result[0]["line"] == 2


def test_analyze_complexity(tmp_path):
    test_file = tmp_path / "example.py"

    test_file.write_text(
        "def calculate(x):\n"
        "    if x > 10:\n"
        "        return x * 2\n"
        "    return x\n",
        encoding="utf-8"
    )

    result = analyze_complexity(test_file)

    assert len(result) == 1
    assert result[0]["function"] == "calculate"
    assert result[0]["complexity"] == 2



def test_detect_structures(tmp_path):
    test_file = tmp_path / "example.py"

    test_file.write_text(
        "class Calculator:\n"
        "    def add(self, a, b):\n"
        "        return a + b\n",
        encoding="utf-8"
    )

    result = detect_structures(test_file)

    assert result["classes"] == ["Calculator"]
    assert result["functions"] == ["add"]


def test_detect_long_functions(tmp_path):
    test_file = tmp_path / "example.py"

    test_file.write_text(
        "def calculate():\n"
        "    x = 1\n"
        "    y = 2\n"
        "    return x + y\n",
        encoding="utf-8"
    )

    result = detect_long_functions(test_file, max_lines=3)

    assert len(result) == 1
    assert result[0]["name"] == "calculate"
    assert result[0]["start_line"] == 1
    assert result[0]["length"] == 4
