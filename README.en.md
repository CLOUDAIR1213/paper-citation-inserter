# Paper Citation Inserter

Codex skill for inserting and repairing ordered literature citations in Word paper documents.

It is designed for Chinese or bilingual academic `.docx` papers that use GB/T 7714 sequential numeric citations. The skill can:

- insert citations from a user-provided literature summary;
- repair citation numbering after paper content changes;
- reorder the final reference list by first citation appearance in the text;
- format generated in-text citation markers as superscript;
- extract citation contexts for semantic alignment review;
- reuse the same number for repeated citations;
- report unused bibliography entries and missing reference entries.

## Install

Install this repository as a Codex skill:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo CLOUDAIR1213/paper-citation-inserter \
  --path . \
  --name paper-citation-inserter
```

Restart Codex after installation.

## Requirements

```bash
pip install -r requirements.txt
```

Core dependencies:

- `python-docx`
- `pypdf`
- `pdfplumber`

## Common Workflows

Extract paper paragraphs and existing citation markers:

```bash
python scripts/extract_docx_paragraphs.py paper.docx --output paper_paragraphs.json
```

Extract the existing bibliography into raw text and JSON:

```bash
python scripts/extract_bibliography.py paper.docx --json bibliography.json --raw bibliography_raw.txt
```

Repair citation order and reorder the bibliography:

```bash
python scripts/repair_citation_order.py paper.docx \
  --output paper_citation_repaired.docx \
  --report paper_citation_report.md
```

Apply an explicit citation insertion plan, then rebuild final citation order:

```bash
python scripts/apply_citation_plan.py paper.docx citation_plan.json \
  --output paper_with_citations.docx \
  --report paper_citation_report.md
```

Extract literature notes from `.docx`, `.txt`, or text-based `.pdf`:

```bash
python scripts/extract_reference_notes.py literature_summary.docx --output reference_entries.json
```

Extract citation contexts for semantic alignment review:

```bash
python scripts/extract_citation_contexts.py paper.docx \
  --reference-notes reference_entries.json \
  --output citation_contexts.json \
  --markdown citation_contexts.md
```

Codex should use `citation_contexts.json` to produce:

- `citation_alignment_review.md`
- `citation_revision_plan.json`

Semantic review is non-mutating by default. It reports weak, mismatched, imprecise, or overly broad citations and proposes a revision plan for later confirmation.

## Citation Rules

- Number references by first appearance in the main text.
- Format in-text citation markers as superscript in generated `.docx` files. Consecutive numbers are compressed with `-`, such as `[1-3]`; commas are used only for non-consecutive numbers, such as `[1-3,5]`.
- Reuse the same number when the same source is cited again.
- Treat the original bibliography order as source data only.
- Rewrite the final bibliography so it matches the rebuilt text citation order.
- Move bibliography entries that are not cited in the text into the report.
- Do not invent missing reference metadata.

## Test

```bash
python -m unittest discover -s tests
```
