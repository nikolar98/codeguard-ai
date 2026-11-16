
def calculate_quality_score(
    bugs,
    long_lines,
    long_functions,
    complexity_results,
    duplicate_blocks
):
    score = 100

    severity_penalties = {
        "HIGH": 15,
        "MEDIUM": 8,
        "LOW": 3
    }

    for bug in bugs:
        severity = bug.get("severity", "LOW")
        score -= severity_penalties.get(severity, 3)

    score -= len(long_lines) * 1
    score -= len(long_functions) * 5
    score -= len(duplicate_blocks) * 4

    for result in complexity_results:
        if result.get("complexity", 0) > 10:
            score -= 5

    score = max(0, score)

    if score >= 90:
        rating = "Excellent"
    elif score >= 75:
        rating = "Good"
    elif score >= 50:
        rating = "Fair"
    else:
        rating = "Poor"

    return {
        "score": score,
        "rating": rating
    }
