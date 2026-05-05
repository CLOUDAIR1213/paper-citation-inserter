from __future__ import annotations

import re
from dataclasses import dataclass


CITATION_PATTERN = re.compile(r"[\[［]([0-9０-９,\-–—，、\s]+)[\]］]")
REFERENCE_HEADING_PATTERN = re.compile(r"^\s*(参考文献|references|bibliography)\s*$", re.IGNORECASE)
LEADING_REFERENCE_NUMBER_PATTERN = re.compile(
    r"^\s*(?:[\[［]?\s*(?P<number>[0-9０-９]+)\s*[\]］]?[\.\．、]?)\s*(?P<body>.*)$"
)
SENTENCE_PATTERN = re.compile(r"[^。！？.!?]+[。！？.!?]?")


def to_ascii_digits(value: str) -> str:
    return value.translate(str.maketrans("０１２３４５６７８９", "0123456789"))


def is_reference_heading(text: str) -> bool:
    return bool(REFERENCE_HEADING_PATTERN.match(text.strip()))


def is_probable_heading(style_name: str, text: str) -> bool:
    clean = text.strip()
    lower_style = style_name.lower()
    if not clean:
        return False
    if lower_style.startswith("heading") or lower_style.startswith("标题"):
        return True
    if is_reference_heading(clean):
        return True
    return bool(re.match(r"^(第[一二三四五六七八九十\d]+[章节]|[一二三四五六七八九十\d]+[\.、]\s*)", clean))


def parse_citation_numbers(raw_inner: str) -> list[int]:
    normalized = to_ascii_digits(raw_inner).replace("，", ",").replace("、", ",")
    normalized = normalized.replace("–", "-").replace("—", "-")
    numbers: list[int] = []
    for part in normalized.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_raw, end_raw = [item.strip() for item in part.split("-", 1)]
            if start_raw.isdigit() and end_raw.isdigit():
                start, end = int(start_raw), int(end_raw)
                step = 1 if end >= start else -1
                numbers.extend(range(start, end + step, step))
            continue
        if part.isdigit():
            numbers.append(int(part))
    return numbers


def find_citation_markers(text: str) -> list[dict]:
    markers = []
    for match in CITATION_PATTERN.finditer(text):
        markers.append(
            {
                "raw": match.group(0),
                "start": match.start(),
                "end": match.end(),
                "numbers": parse_citation_numbers(match.group(1)),
            }
        )
    return markers


def format_citation_numbers(numbers: list[int]) -> str:
    unique = []
    for number in numbers:
        if number not in unique:
            unique.append(number)
    return "[" + ",".join(str(number) for number in unique) + "]"


def set_paragraph_text_with_superscript_citations(paragraph, text: str) -> None:
    paragraph.text = ""
    position = 0
    for match in CITATION_PATTERN.finditer(text):
        if match.start() > position:
            paragraph.add_run(text[position : match.start()])
        run = paragraph.add_run(match.group(0))
        run.font.superscript = True
        position = match.end()
    if position < len(text):
        paragraph.add_run(text[position:])


@dataclass
class ReferenceEntry:
    original_number: int | None
    text: str

    def renumbered(self, new_number: int) -> str:
        return f"[{new_number}] {strip_leading_reference_number(self.text)}"


def strip_leading_reference_number(text: str) -> str:
    match = LEADING_REFERENCE_NUMBER_PATTERN.match(text.strip())
    if not match:
        return text.strip()
    return match.group("body").strip()


def parse_reference_line(text: str) -> tuple[int | None, str]:
    match = LEADING_REFERENCE_NUMBER_PATTERN.match(text.strip())
    if not match:
        return None, text.strip()
    return int(to_ascii_digits(match.group("number"))), match.group("body").strip()


def split_sentences(text: str) -> list[str]:
    return [match.group(0).strip() for match in SENTENCE_PATTERN.finditer(text) if match.group(0).strip()]


def normalize_reference_key(text: str) -> str:
    body = strip_leading_reference_number(text)
    body = re.sub(r"\s+", " ", body).strip().lower()
    return body[:240]
