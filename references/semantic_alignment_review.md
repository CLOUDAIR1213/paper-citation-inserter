# Semantic Alignment Review Template

Use this template when reviewing whether正文 citations support their sentence or paragraph.

## Output files

- `citation_alignment_review.md`
- `citation_revision_plan.json`

## Report structure

```markdown
# 引用语义对齐检查报告

检查对象：`paper.docx`

## 总体结论

说明编号层面是否一致，文末参考文献是否按正文顺序对应，以及语义层面发现的问题数量和类型。

## 需要优先修正

列出明显不匹配或会影响论文规范性的引用问题。

### 1. 段落 N：引用 [x] 与句子主题不匹配

正文句子：

> ...

当前文末 [x]：

> ...

判断：明显不匹配 / 支撑偏弱 / 引用位置不精准 / 合并引用过宽 / 待人工确认。

建议：替换为 [y]、补充 [z]、移到其他句子、缩小为 [a-b]，或人工确认。

## 建议优化

列出支撑偏弱、位置不够精准、合并引用过宽但不一定必须修正的问题。

## 基本对齐的引用

按编号或编号范围简要列出基本匹配的引用。

## 结论

总结是否满足顺序编码要求，以及下一步建议优先处理哪些引用。
```

## Judgment labels

- `明显不匹配`: cited source does not support the sentence or paragraph theme.
- `支撑偏弱`: cited source is generally related but does not directly support the claim.
- `引用位置不精准`: source is useful but should be moved to a different sentence or paragraph.
- `合并引用过宽`: a range such as `[36-39]` contains one or more sources that do not support the exact claim.
- `基本对齐`: source supports the claim well enough.
- `待人工确认`: context or metadata is insufficient for a confident judgment.

## Recommendation types

- `replace_citation`: replace the current citation with a better one.
- `add_citation`: add a stronger supporting citation.
- `remove_citation`: remove a citation that does not support the claim.
- `narrow_range`: reduce a merged citation range, such as `[36-39]` to `[37-39]`.
- `move_citation`: move a citation to a more suitable sentence or paragraph.
- `manual_review`: mark for human confirmation.
