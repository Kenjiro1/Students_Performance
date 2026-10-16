"""Summarize public OULAD assessment metadata by module presentation."""

import argparse
import csv
from pathlib import Path


FIELDS = [
    "code_module", "code_presentation", "module_presentation_length",
    "assessment_count", "tma_count", "cma_count", "exam_count",
    "dated_assessment_count", "earliest_due_day", "latest_due_day",
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("courses", type=Path, help="Original OULAD courses.csv")
    parser.add_argument("assessments", type=Path, help="Original OULAD assessments.csv")
    parser.add_argument("output", type=Path, help="Summary CSV to create")
    args = parser.parse_args()
    if args.output.resolve() in {args.courses.resolve(), args.assessments.resolve()}:
        parser.error("Output must be different from each input")

    summary = {}
    with args.courses.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != FIELDS[:3]:
            parser.error(f"Unexpected courses.csv schema: {reader.fieldnames}")
        for row in reader:
            key = (row["code_module"], row["code_presentation"])
            if key in summary:
                raise ValueError(f"Duplicate course presentation: {key}")
            summary[key] = {
                "code_module": key[0],
                "code_presentation": key[1],
                "module_presentation_length": row["module_presentation_length"],
                "assessment_count": 0,
                "tma_count": 0,
                "cma_count": 0,
                "exam_count": 0,
                "dated_assessment_count": 0,
                "earliest_due_day": "",
                "latest_due_day": "",
            }

    with args.assessments.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        expected = [
            "code_module", "code_presentation", "id_assessment",
            "assessment_type", "date", "weight",
        ]
        if reader.fieldnames != expected:
            parser.error(f"Unexpected assessments.csv schema: {reader.fieldnames}")
        for row in reader:
            key = (row["code_module"], row["code_presentation"])
            item = summary[key]
            kind = row["assessment_type"]
            if kind not in {"TMA", "CMA", "Exam"}:
                raise ValueError(f"Unexpected assessment type: {kind}")
            item["assessment_count"] += 1
            item[{"TMA": "tma_count", "CMA": "cma_count", "Exam": "exam_count"}[kind]] += 1
            if row["date"]:
                day = int(row["date"])
                item["dated_assessment_count"] += 1
                first = item["earliest_due_day"]
                last = item["latest_due_day"]
                item["earliest_due_day"] = min(day, first) if first != "" else day
                item["latest_due_day"] = max(day, last) if last != "" else day

    with args.output.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target, fieldnames=FIELDS, quoting=csv.QUOTE_ALL, lineterminator="\r\n"
        )
        writer.writeheader()
        writer.writerows(summary.values())
    print(f"Created {args.output}: {len(summary)} course presentations")


if __name__ == "__main__":
    main()
