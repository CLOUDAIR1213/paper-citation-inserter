---
name: paper-citation-inserter
description: Insert, repair, and review ordered literature citations in Word论文 documents. Use when Codex needs to add references to a .docx paper from a literature summary, rebuild GB/T 7714 顺序编码 superscript citations, reorder文末参考文献 by first正文 appearance, fix mismatched正文 citations and bibliography entries, report unused references, flag正文引用但文末缺失的条目, perform 引用语义对齐/citation alignment review, identify 引用支撑不足、引用不匹配、引用位置不精准, or narrow 合并引用过宽 ranges.
---

# Paper Citation Inserter

## Purpose

Use this skill for Chinese or bilingual academic论文 `.docx` files that need GB/T 7714 顺序编码 citation insertion, citation-order repair, or citation semantic alignment review. The default rule is: number citations by first appearance in正文, show正文 citation markers as superscript `[6,9]` style, reuse the same number for repeated citations, and make文末参考文献 match that final order.

Do not invent missing文献信息. If metadata is absent, keep the known fields and report what needs optional联网补全.

## Workflow

1. Identify the task type:
   - **Repair existing citations**:正文 already has citation markers and文末参考文献 exists, but numbering/order may be wrong after content edits.
   - **Insert new citations**: the user provides a paper plus a literature summary or a citation plan.
   - **Semantic alignment review**:正文 citations are already numbered, but the user needs to check whether each cited reference actually supports its sentence or paragraph.
   - **Mixed task**: insert new citations, then rebuild all numbering and references.
2. Preserve the original paper. Always write a new `.docx`.
3. Extract structure before editing:
   - Run `scripts/extract_docx_paragraphs.py <paper.docx> --output paper_paragraphs.json`.
   - Run `scripts/extract_bibliography.py <paper.docx> --json bibliography.json --raw bibliography_raw.txt`.
   - If external literature notes are provided, run `scripts/extract_reference_notes.py <notes.docx|txt|pdf> --output reference_entries.json`.
   - For semantic review, run `scripts/extract_citation_contexts.py <paper.docx> --reference-notes reference_entries.json --output citation_contexts.json --markdown citation_contexts.md`.
4. For semantic insertion, create a citation plan from正文 claims to literature entries. Insert only high-confidence matches; put uncertain matches in the report as 待确认候选.
5. For semantic alignment review, use `citation_contexts.json` plus `references/semantic_alignment_review.md` to produce `citation_alignment_review.md` and `citation_revision_plan.json`. Do not directly modify `.docx` during review unless the user explicitly approves the revision plan.
6. Rebuild order after every insertion or repair:
   - Run `scripts/repair_citation_order.py <paper.docx> --output <paper>_citation_repaired.docx --report <paper>_citation_report.md`.
   - For explicit insertion plans, run `scripts/apply_citation_plan.py <paper.docx> <citation_plan.json> --output <paper>_with_citations.docx --report <paper>_citation_report.md`.

## Core Rules

- Read all existing文末 references first and treat them as a temporary reference library.
- Treat original文末 order only as source data; final order must follow正文 first appearance.
- Scan正文 from beginning to end. The first unique cited文献 becomes `[1]`, the next unique cited文献 becomes `[2]`, and so on.
- Format正文 citation markers as superscript in generated `.docx` files. Multiple citations in one marker use comma style such as superscript `[6,9]`, not separate `[6][9]` markers.
- Repeated citations to the same文献 reuse their assigned number.
- Rebuild existing citation markers instead of preserving old numbering.
- Reorder文末参考文献 to exactly match rebuilt正文 numbering.
- Remove文末 entries that are not cited in正文 from the final reference list and report them under “文末存在但正文未引用”.
- If正文 cites an old number with no matching文末 entry, do not fabricate a reference. Leave it for review and report it under “正文引用但文末缺失”.
- Keep citation density conservative: usually 1-3 references for one claim or sentence.

## Semantic Alignment Review

Use this review mode when the user asks whether citations are appropriate, aligned, supportive, misplaced, too broad, or semantically wrong.

1. First confirm numbering consistency using the extracted citation contexts and bibliography mapping.
2. Then judge semantic support for each citation against the cited sentence, paragraph context,文末 reference, and optional literature summary.
3. Classify issues with these labels: 明显不匹配, 支撑偏弱, 引用位置不精准, 合并引用过宽, 基本对齐, 待人工确认.
4. Output `citation_alignment_review.md` using the structure in `references/semantic_alignment_review.md`.
5. Output `citation_revision_plan.json` using `references/citation_revision_plan_schema.json`.
6. Keep semantic review non-mutating by default. The revision plan is input for a later edit step, not automatic proof that the document should be changed.

## Citation Plan Format

Use this JSON shape for `apply_citation_plan.py` when a semantic matching pass has selected insertions:

```json
{
  "insertions": [
    {
      "paragraph_index": 12,
      "sentence": "Optional sentence to match",
      "reference_text": "Author. Title[J]. Journal, Year, Volume(Issue): Pages.",
      "reason": "This source supports the claim about model performance",
      "confidence": "high"
    }
  ],
  "candidates": [
    {
      "paragraph_index": 18,
      "reference_text": "Low-confidence candidate reference",
      "reason": "Related but not strong enough to insert"
    }
  ]
}
```

`reference_text` may be an existing文末 entry or a new literature entry from the summary. The script assigns temporary numbers, inserts markers, then repairs final顺序编号.

## Reports

The Markdown report must include:

- old citation number and rebuilt citation number;
- section or paragraph index and original sentence where available;
- matched文末 reference entry;
- unused文末 references;
-正文引用但文末缺失的待补条目;
- semantic insertions and low-confidence candidates, if applicable.

## References

Read `references/gbt7714.md` when formatting or checking GB/T 7714 顺序编码 references.
Read `references/semantic_alignment_review.md` when writing semantic review reports.
Read `references/citation_revision_plan_schema.json` when producing machine-readable revision plans.
