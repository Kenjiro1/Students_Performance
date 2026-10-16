"""Add coherent illustrative titles to the original OULAD VLE table.

The added `title` is synthetic, not the source resource title or content.
Examples are selected by activity type and made identifiable using metadata.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path


ORIGINAL_COLUMNS = [
    "id_site",
    "code_module",
    "code_presentation",
    "activity_type",
    "week_from",
    "week_to",
]

EXAMPLE_TITLES = {
    "resource": (
        "Learning resource for reviewing course concepts",
        "Supplementary study material for this module",
        "Course resource for independent study",
        "Supporting material for a learning activity",
        "Learning resource for lesson review",
        "Reference material for course study",
    ),
    "subpage": (
        "Course subpage for learning materials",
        "Course subpage for study activities",
        "Course subpage for navigating resources",
    ),
    "oucontent": (
        "Course content page for lesson study",
        "Course content for reviewing learning material",
        "Lesson content and study activities",
        "Course content for guided study",
    ),
    "url": (
        "External link to a supporting learning resource",
        "External link for further course study",
        "External reference link for this module",
    ),
    "forumng": (
        "Discussion forum for course questions",
        "Forum for peer discussion of study activities",
        "Forum for clarifying learning tasks",
        "Course forum for exchanging explanations",
        "Discussion forum for reviewing course ideas",
    ),
    "quiz": (
        "Practice quiz for checking understanding",
        "Self-check quiz for lesson review",
        "Course quiz for independent practice",
    ),
    "page": (
        "Course page with learning information",
        "Learning page for this module",
        "Course page for study activities",
    ),
    "oucollaborate": (
        "Collaborative online study activity",
        "Group learning space for course discussion",
        "Collaborative session for sharing ideas",
    ),
    "questionnaire": (
        "Course questionnaire for learner responses",
        "Questionnaire related to this module",
    ),
    "ouwiki": (
        "Collaborative wiki for course notes",
        "Shared wiki for organizing learning ideas",
        "Course wiki for jointly edited material",
    ),
    "dataplus": ("DataPlus course activity",),
    "externalquiz": ("External quiz for course practice",),
    "homepage": ("Course homepage for module navigation",),
    "glossary": (
        "Course glossary for key terms",
        "Glossary for reviewing course vocabulary",
    ),
    "ouelluminate": ("Elluminate online course activity",),
    "dualpane": ("Dual-pane course activity",),
    "repeatactivity": ("Repeated course activity",),
    "htmlactivity": ("HTML learning activity",),
    "sharedsubpage": ("Shared course subpage",),
    "folder": ("Folder of course learning resources",),
}


def make_title(row):
    """Pick a complete activity example; append only observed identifiers."""
    activity_type = row["activity_type"]
    options = EXAMPLE_TITLES.get(activity_type, (f"Course activity ({activity_type})",))
    digest = hashlib.sha256(row["id_site"].encode("ascii")).digest()
    example = options[int.from_bytes(digest[:8], "big") % len(options)]
    parts = [
        example,
        f"module {row['code_module']} ({row['code_presentation']})",
    ]
    start, end = row["week_from"], row["week_to"]
    if start.isdecimal() and end.isdecimal():
        if start == end:
            parts.append(f"planned week {start}")
        else:
            parts.append(f"planned weeks {start}-{end}")
    parts.append(f"VLE site {row['id_site']}")
    return " | ".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Original six-column OULAD vle.csv")
    parser.add_argument("output", type=Path, help="Output seven-column vle.csv")
    parser.add_argument("--titles-json", type=Path, help="Optional id_site-to-label map")
    args = parser.parse_args()

    if args.source.resolve() == args.output.resolve():
        parser.error("Choose an output path distinct from the original source")

    title_map = {}
    with args.source.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != ORIGINAL_COLUMNS:
            parser.error(f"Expected source columns {ORIGINAL_COLUMNS}, got {reader.fieldnames}")
        with args.output.open("w", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(
                output,
                fieldnames=ORIGINAL_COLUMNS + ["title"],
                quoting=csv.QUOTE_ALL,
                lineterminator="\r\n",
            )
            writer.writeheader()
            count = 0
            for row in reader:
                row["title"] = make_title(row)
                title_map[row["id_site"]] = row["title"]
                writer.writerow(row)
                count += 1

    if args.titles_json:
        args.titles_json.write_text(
            json.dumps(title_map, ensure_ascii=False, sort_keys=True), encoding="utf-8"
        )
    print(f"Created {args.output} with {count} illustrative resource titles")


if __name__ == "__main__":
    main()
