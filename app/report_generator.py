import json


def generate_json_report(data, output_file="report.json"):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"JSON report generated: {output_file}")
