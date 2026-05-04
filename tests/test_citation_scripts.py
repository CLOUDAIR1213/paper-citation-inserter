from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from repair_citation_order import repair_document
from apply_citation_plan import apply_plan_to_copy


def paragraph_texts(path: Path) -> list[str]:
    return [paragraph.text for paragraph in Document(str(path)).paragraphs]


class CitationScriptTests(unittest.TestCase):
    def make_docx(self, path: Path) -> None:
        doc = Document()
        doc.add_heading("绪论", level=1)
        doc.add_paragraph("第二篇文献先在正文出现[2]，后面又引用第一篇文献[1]。")
        doc.add_paragraph("第二篇文献再次出现时仍应复用编号[2]。")
        doc.add_paragraph("这一句引用了不存在的文献[9]。")
        doc.add_heading("参考文献", level=1)
        doc.add_paragraph("[1] Zhang A. First source[J]. Journal, 2020, 1(1): 1-5.")
        doc.add_paragraph("[2] Li B. Second source[J]. Journal, 2021, 2(1): 6-9.")
        doc.add_paragraph("[3] Wang C. Unused source[J]. Journal, 2022, 3(1): 10-12.")
        doc.save(str(path))

    def test_repair_order_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "paper.docx"
            output = Path(tmp) / "paper_repaired.docx"
            report = Path(tmp) / "report.md"
            self.make_docx(source)

            repair_document(source, output, report)

            texts = paragraph_texts(output)
            self.assertIn("第二篇文献先在正文出现[1]，后面又引用第一篇文献[2]。", texts)
            self.assertIn("第二篇文献再次出现时仍应复用编号[1]。", texts)
            self.assertIn("[1] Li B. Second source", "\n".join(texts))
            self.assertIn("[2] Zhang A. First source", "\n".join(texts))
            self.assertNotIn("[3] Wang C. Unused source", "\n".join(texts))

            report_text = report.read_text(encoding="utf-8")
            self.assertIn("Wang C. Unused source", report_text)
            self.assertIn("原正文引用编号 [9]", report_text)

    def test_apply_plan_adds_reference_then_repairs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "paper.docx"
            working = Path(tmp) / "working.docx"
            plan = Path(tmp) / "plan.json"
            self.make_docx(source)
            plan.write_text(
                json.dumps(
                    {
                        "insertions": [
                            {
                                "paragraph_index": 1,
                                "reference_text": "Chen D. New source[J]. Journal, 2024, 4(1): 13-18.",
                                "reason": "supports the opening claim",
                                "confidence": "high",
                            }
                        ],
                        "candidates": [],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            apply_plan_to_copy(source, plan, working)

            texts = paragraph_texts(working)
            self.assertTrue(any("Chen D. New source" in text for text in texts))
            self.assertTrue(any("[4]" in text for text in texts))


if __name__ == "__main__":
    unittest.main()
