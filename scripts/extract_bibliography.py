from __future__ import annotations

import argparse
import json
from pathlib import Path

from docx import Document

from citation_utils import ReferenceEntry, is_reference_heading, parse_reference_line


def extract_bibliography_entries(path: Path) -> tuple[list[ReferenceEntry], int | None]:
    doc = Document(str(path))
    entries: list[ReferenceEntry] = []
    current_number: int | None = None
    current_parts: list[str] = []
    bibliography_start: int | None = None

    for index, paragraph in enumerate(doc.paragraphs):
        text = paragraph.text.strip()
        if bibliography_start is None:
            if is_reference_heading(text):
                bibliography_start = index
            continue
        if not text:
            continue

        number, body = parse_reference_line(text)
        if number is not None:
            if current_parts:
                entries.append(ReferenceEntry(current_number, " ".join(current_parts).strip()))
            current_number = number
            current_parts = [f"[{number}] {body}"]
        elif current_parts:
            current_parts.append(text)
        else:
            entries.append(ReferenceEntry(None, text))

    if current_parts:
        entries.append(ReferenceEntry(current_number, " ".join(current_parts).strip()))

    return entries, bibliography_start


def entries_to_json(entries: list[ReferenceEntry], source: Path, bibliography_start: int | None) -> dict:
    return {
        "source": str(source),
        "bibliography_start_paragraph": bibliography_start,
        "entries": [
            {
                "original_number": entry.original_number,
                "text": entry.text,
            }
            for entry in entries
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract the References/参考文献 section from a .docx file.")
    parser.add_argument("docx", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path, default=Path("bibliography.json"))
    parser.add_argument("--raw", dest="raw_path", type=Path, default=Path("bibliography_raw.txt"))
    args = parser.parse_args()

    entries, bibliography_start = extract_bibliography_entries(args.docx)
    args.json_path.write_text(
        json.dumps(entries_to_json(entries, args.docx, bibliography_start), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    args.raw_path.write_text("\n".join(entry.text for entry in entries), encoding="utf-8")
    print(f"Wrote {args.json_path} and {args.raw_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
