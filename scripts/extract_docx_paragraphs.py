from __future__ import annotations

import argparse
import json
from pathlib import Path

from docx import Document

from citation_utils import find_citation_markers, is_probable_heading, is_reference_heading, split_sentences


def extract_docx_paragraphs(path: Path) -> dict:
    doc = Document(str(path))
    paragraphs = []
    current_section = ""
    in_bibliography = False

    for index, paragraph in enumerate(doc.paragraphs):
        text = paragraph.text.strip()
        style_name = paragraph.style.name if paragraph.style else ""
        is_heading = is_probable_heading(style_name, text)
        if is_reference_heading(text):
            in_bibliography = True
            current_section = text
        elif is_heading:
            current_section = text

        paragraphs.append(
            {
                "index": index,
                "style": style_name,
                "text": text,
                "section": current_section,
                "is_heading": is_heading,
                "is_bibliography": in_bibliography,
                "citations": find_citation_markers(text),
                "sentences": split_sentences(text),
            }
        )

    return {"source": str(path), "paragraphs": paragraphs}


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract .docx paragraph structure and citation markers.")
    parser.add_argument("docx", type=Path)
    parser.add_argument("--output", "-o", type=Path, default=Path("paper_paragraphs.json"))
    args = parser.parse_args()

    data = extract_docx_paragraphs(args.docx)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
