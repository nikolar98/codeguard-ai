
from app.analyzers.bug_detector import (
    detect_bare_except,
    detect_mutable_defaults
)


def test_detect_bare_except(tmp_path):
    test_file = tmp_path / "example.py"

    test_file.write_text(
        "try:\n"
        "    x = 10 / 0\n"
        "except:\n"
        "    print('Error')\n",
        encoding="utf-8"
    )

    bugs = detect_bare_except(test_file)

    assert len(bugs) == 1
    assert bugs[0]["line"] == 3
    assert bugs[0]["type"] == "bare_except"


def test_no_bare_except(tmp_path):
    test_file = tmp_path / "example.py"

    test_file.write_text(
        "try:\n"
        "    x = 10 / 0\n"
        "except ZeroDivisionError:\n"
        "    print('Error')\n",
        encoding="utf-8"
    )

    bugs = detect_bare_except(test_file)

    assert bugs == []


def test_detect_mutable_defaults(tmp_path):
    test_file = tmp_path / "example.py"

    test_file.write_text(
        "def add_item(item, items=[]):\n"
        "    items.append(item)\n"
        "    return items\n",
        encoding="utf-8"
    )

    bugs = detect_mutable_defaults(test_file)

    assert len(bugs) == 1
    assert bugs[0]["line"] == 1
    assert bugs[0]["type"] == "mutable_default"


def test_no_mutable_defaults(tmp_path):
    test_file = tmp_path / "example.py"

    test_file.write_text(
        "def add_item(item, items=None):\n"
        "    if items is None:\n"
        "        items = []\n"
        "    items.append(item)\n"
        "    return items\n",
        encoding="utf-8"
    )

    bugs = detect_mutable_defaults(test_file)

    assert bugs == []
