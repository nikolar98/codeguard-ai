
from app.analyzers.quality_scorer import calculate_quality_score


def calculate(bugs=None, long_lines=None, long_functions=None,
              complexity=None, duplicates=None):
    return calculate_quality_score(
        bugs or [],
        long_lines or [],
        long_functions or [],
        complexity or [],
        duplicates or []
    )


def test_perfect_score():
    result = calculate()

    assert result["score"] == 100
    assert result["rating"] == "Excellent"


def test_high_severity_bug():
    result = calculate(bugs=[{"severity": "HIGH"}])

    assert result["score"] == 85
    assert result["rating"] == "Good"


def test_medium_and_low_severity():
    result = calculate(bugs=[
        {"severity": "MEDIUM"},
        {"severity": "LOW"}
    ])

    assert result["score"] == 89
    assert result["rating"] == "Good"


def test_long_lines_and_functions():
    result = calculate(
        long_lines=[{}, {}],
        long_functions=[{}]
    )

    assert result["score"] == 93
    assert result["rating"] == "Excellent"


def test_high_complexity():
    result = calculate(
        complexity=[{"complexity": 12}]
    )

    assert result["score"] == 95


def test_duplicate_blocks():
    result = calculate(duplicates=[{}, {}, {}])

    assert result["score"] == 88
    assert result["rating"] == "Good"


def test_minimum_score():
    result = calculate(
        bugs=[{"severity": "HIGH"}] * 10
    )

    assert result["score"] == 0
    assert result["rating"] == "Poor"


def test_rating_boundaries():
    assert calculate(long_lines=[{}] * 10)["rating"] == "Excellent"
    assert calculate(long_lines=[{}] * 25)["rating"] == "Good"
    assert calculate(long_lines=[{}] * 50)["rating"] == "Fair"
    assert calculate(long_lines=[{}] * 51)["rating"] == "Poor"
