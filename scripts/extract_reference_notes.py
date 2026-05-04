from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from docx import Document

from citation_utils import parse_reference_line


def read_docx(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(paragraph.text.strip() for paragraph in doc.paragraphs if paragraph.text.strip())


def read_pdf(path: Path) -> str:
    try:
        import pdfplumber

        with pdfplumber.open(str(path)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return read_docx(path)
    if suffix == ".pdf":
        return read_pdf(path)
    return path.read_text(encoding="utf-8")


def split_entries(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    entries: list[str] = []
    current: list[str] = []

    for line in lines:
        if not line:
            if current:
                entries.append(" ".join(current).strip())
                current = []
            continue
        number, body = parse_reference_line(line)
        if number is not None and current:
            entries.append(" ".join(current).strip())
            current = [body]
        else:
            current.append(body if number is not None else line)

    if current:
        entries.append(" ".join(current).strip())
    return [entry for entry in entries if entry]


def extract_metadata(raw: str) -> dict:
    doi_match = re.search(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", raw, re.IGNORECASE)
    year_match = re.search(r"\b(19|20)\d{2}\b", raw)
    title = raw.split(".")[0].strip() if "." in raw else raw[:80].strip()
    missing = []
    if not year_match:
        missing.append("year")
    if not doi_match:
        missing.append("doi")
    return {
        "title_guess": title,
        "year": year_match.group(0) if year_match else None,
        "doi": doi_match.group(0) if doi_match else None,
        "missing_metadata": missing,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract literature summary entries from .docx, .txt, or text-based .pdf.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", "-o", type=Path, default=Path("reference_entries.json"))
    args = parser.parse_args()

    text = read_text(args.source)
    entries = split_entries(text)
    data = {
        "source": str(args.source),
        "entries": [
            {
                "source_id": f"R{index}",
                "raw_text": raw,
                **extract_metadata(raw),
            }
            for index, raw in enumerate(entries, start=1)
        ],
    }
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
