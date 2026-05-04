# Paper Citation Inserter

用于 Word 论文文档的 Codex skill，支持插入文献引用和修复顺序编码引用。

该 skill 面向使用 GB/T 7714 顺序编码制的中文或中英双语 `.docx` 学术论文。它可以：

- 根据用户提供的文献汇总插入引用；
- 在论文内容修改后修复正文引用编号；
- 按正文首次引用顺序重排文末参考文献；
- 对同一篇文献的重复引用复用同一个编号；
- 报告文末存在但正文未引用的文献；
- 报告正文引用但文末缺失的文献条目。

## 安装

将本仓库安装为 Codex skill：

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/CLOUDAIR1213/paper-citation-inserter/tree/main
```

安装后重启 Codex。

## 依赖

```bash
pip install -r requirements.txt
```

核心依赖：

- `python-docx`
- `pypdf`
- `pdfplumber`

## 常用流程

提取论文段落和已有正文引用标记：

```bash
python scripts/extract_docx_paragraphs.py paper.docx --output paper_paragraphs.json
```

将已有文末参考文献提取为原始文本和 JSON：

```bash
python scripts/extract_bibliography.py paper.docx --json bibliography.json --raw bibliography_raw.txt
```

修复正文引用顺序并重排文末参考文献：

```bash
python scripts/repair_citation_order.py paper.docx \
  --output paper_citation_repaired.docx \
  --report paper_citation_report.md
```

应用明确的引用插入计划，然后重建最终引用顺序：

```bash
python scripts/apply_citation_plan.py paper.docx citation_plan.json \
  --output paper_with_citations.docx \
  --report paper_citation_report.md
```

从 `.docx`、`.txt` 或文本型 `.pdf` 中提取文献笔记：

```bash
python scripts/extract_reference_notes.py literature_summary.docx --output reference_entries.json
```

## 引用规则

- 按正文首次出现顺序给文献编号。
- 同一文献再次出现时复用原编号。
- 原文末参考文献顺序只作为来源数据，不作为最终顺序。
- 最终文末参考文献必须和正文重建后的引用顺序一致。
- 文末有但正文没有引用的文献移入报告，不放入最终编号列表。
- 不编造缺失的文献信息。

## 测试

```bash
python -m unittest discover -s tests
```
