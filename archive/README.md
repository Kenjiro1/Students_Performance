# OULAD resource and assessment metadata for reproducible tests

**Suggested Kaggle title:** OULAD Resource and Assessment Metadata

## Overview

This package brings together two linked views of the public Open University Learning Analytics Dataset (OULAD): virtual learning environment (VLE) resource metadata and a course-presentation assessment summary. The files support reproducible tests of CSV loading, cross-table joins, assessment aggregation, and text-processing workflows. Researchers can link the two outputs using `code_module` and `code_presentation`.

The resource file keeps the original VLE rows and adds a **synthetic** `title` field for software that expects descriptive resource text. The separate summary derives assessment counts and available date ranges from OULAD's original `courses.csv` and `assessments.csv`. The titles are illustrative placeholders, not actual resource names or course topics. The package also includes the other six OULAD tables, including learner-level records and interaction logs.

## Source and credit

The source is the Open University Learning Analytics Dataset (OULAD), described by Kuzilek, J., Hlosta, M., and Zdrahal, Z. (2017), *Open University Learning Analytics dataset*, Scientific Data 4, 170171. https://doi.org/10.1038/sdata.2017.171 . Original dataset page: https://research.stem.open.ac.uk/ouanalyse/dataset/ . The original data are released under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/ . Please credit the original authors and identify the synthetic resource titles and derived assessment summary as modifications.

Input: the original OULAD `vle.csv` used to prepare this package, SHA-256 `d7a146497edd0e47ef536144b58796c07b554002d3753e848b8e4cd8a56f4c38`.

Output: **this package's modified `vle.csv`**, SHA-256 `c2f90a31df60aeddc167299de4e73550737308fdbd252852a5a4db02d5e7dd78`. It has the same filename as the OULAD source but is a different file with an added synthetic `title` column. Keep the original source at a separate path.

Additional input files: the original OULAD `courses.csv`, SHA-256 `4f16eee7454b15e109b0a21a0e43be820e6846ed6f9301bb7feb5ab5ad737a75`, and `assessments.csv`, SHA-256 `9ce92381e4a0ac457f8e251b2eb2c179ed51e023ab30d1d671a0268bd62316ba`.

Additional output: `course_presentation_assessment_summary.csv`, SHA-256 `c0bcd076baa5040f27f50561cda1a78990fb31008404abbf4657caa3218fa6d7`.

This package updates the original OULAD version by adding synthetic resource titles to `vle.csv` and providing a separate derived assessment summary.

## Updates in this release

- Added a synthetic, human-readable `title` field to the original VLE resource table while preserving its existing rows and columns.
- Replaced the earlier concatenated study phrases with complete, short illustrative activity titles.
- Added a separate course-presentation assessment summary derived from the original `courses.csv` and `assessments.csv` tables.
- Included the other six OULAD tables alongside the modified `vle.csv`.

Both updates have documented inputs and generation scripts below so the current files can be recreated and checked.

## Development timeline

Each update replaces the previous dataset package with a new version.

| Date | Update |
| --- | --- |
| **2024-08-10** | Earlier VLE-table updates. |
| **2026-07-12** | Earlier course-assessment summary updates. |
| **2026-09-25** | Dataset updated. |

## Files in this demonstration package

| File | Contents |
| --- | --- |
| `vle.csv` (modified) | Original VLE resource metadata plus one synthetic `title` column; distinct from the source file of the same name. |
| `courses.csv` | Original course and presentation metadata. |
| `assessments.csv` | Original assessment metadata. |
| `studentInfo.csv` | Original learner profiles. |
| `studentRegistration.csv` | Original registration records. |
| `studentAssessment.csv` | Original learner assessment records. |
| `studentVle.csv` | Original learner–resource interaction records. |
| `OULAD.names` | Original description of the OULAD data fields. |
| `course_presentation_assessment_summary.csv` | Course-presentation details with counts and available date ranges derived from original course and assessment metadata. |
| `generate_oulad.py` | Recreates the synthetic-title CSV from original `vle.csv`. |
| `generate_course_assessment_summary.py` | Recreates the assessment summary from original `courses.csv` and `assessments.csv`. |

The learner and interaction tables are included as source data; they were not used to create the two derived output tables.

## How the added field was made

- All 6,364 input rows remain in their original order. The six input columns are preserved, and a seventh column named `title` is added.
- Complete English example titles were drafted with AI assistance for each `activity_type`, with **no access to the resources' real names or contents**. They describe plausible activity uses for testing and do not state what the original materials contain.
- One complete phrase is selected for each resource and followed by the original module, presentation, and `id_site`. The planned week is included only if it is present in that resource's original VLE row.
- The example phrase is selected using a fixed SHA-256-based rule applied to `id_site` so that the same input produces the same output. `id_site` is a selection key, **not** evidence about a resource's topic. The complete lists and rule are in `generate_oulad.py`.

Example of an illustrative title: `Forum for clarifying learning tasks | module AAA (2013J) | VLE site 546658`. This is not the real title of that resource.

To regenerate the CSV from the original OULAD `vle.csv`:

```bash
python generate_oulad.py /path/to/original/vle.csv vle.csv
```

## Course-presentation assessment summary

The companion summary contains one row for each of the **22** `(code_module, code_presentation)` combinations in `courses.csv`. It joins to the modified VLE resource table on these same two fields. It aggregates the **206** source assessment records by presentation: total assessments, counts of TMA, CMA, and Exam entries, number with an available `date`, and the smallest and largest available `date` values. `module_presentation_length` comes directly from `courses.csv`. A missing assessment date (`?` in the original UCI file) does not contribute to the earliest and latest values. These are **course-presentation-level** values, not attributes measured separately for each resource or learner.

| Summary column | Source and calculation |
| --- | --- |
| `code_module`, `code_presentation` | Original join keys from `courses.csv`; also present in `assessments.csv` and the modified VLE table. |
| `module_presentation_length` | Copied without change from the corresponding `courses.csv` row. |
| `assessment_count` | Number of matching rows in `assessments.csv`. |
| `tma_count`, `cma_count`, `exam_count` | Numbers of matching assessments with `assessment_type` equal to `TMA`, `CMA`, or `Exam`, respectively. |
| `dated_assessment_count` | Number of matching assessments with an available `date` value. |
| `earliest_due_day`, `latest_due_day` | Minimum and maximum available `date` values within the presentation. Empty if no date is available. |

Checks on the source files: the 22 presentations account for all 206 assessments (**106 TMA, 76 CMA, 24 Exam**). Of those, **195** have a date and **11** have a missing `date`. Every module-presentation key in the assessment and VLE inputs matches a key in `courses.csv`. No learner ID or score is used in these summary calculations.

Recreate the summary from the two original OULAD tables:

```bash
python generate_course_assessment_summary.py courses.csv assessments.csv course_presentation_assessment_summary.csv
```

## Intended use and limits

These files support inspection of modified resource metadata and experiments with text parsing, indexing, feature extraction, and joins to course assessment summaries. The example phrases were assigned without reading the real learning materials. Their apparent specificity should not be used to make claims about what Open University learners studied or how they interacted. The new summary does not contain individual learner records or assessment scores. Empirical analysis of learner behaviour can use the included original learner and interaction tables with a separate, documented method.
