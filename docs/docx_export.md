# DOCX Export

这份文档定义：当用户要 `导读 docx` 时，`podcast_analysis_doc` 应该如何交付。

## 1. 固定原则

导出 Word 不是第一步，而是最后一步。

固定流程：

1. 先拿到足够文本
2. 先完成 Markdown / 纯文本结构稿
3. 再调用 docx 能力导出 `.docx`

不要跳过中间稿，直接在脑内拼 Word。

## 2. 当前推荐导出链路

这个 skill 当前内置一条 **macOS 友好、零第三方 Python 依赖** 的导出路径：

- 把 Markdown 结构稿转换成简单 HTML
- 再调用系统自带 `textutil` 输出 `.docx`

脚本入口：

```bash
python3 scripts/export_docx.py input.md -o output.docx
```

适用特点：
- 不依赖 `python-docx`
- 不依赖 `pandoc`
- 不依赖 `node`
- 适合导读类文档这种“标题 + 段落 + 列表”结构

限制：
- 当前更适合简洁版式
- 不适合复杂表格、图片、页眉页脚等高级排版

## 3. 什么时候可以导出

满足这些条件时再导出：

- 标题已确定
- 摘要已完成
- 章节速览已完成
- 是否包含增强分析已确定
- 文件名已确定或可默认命名

## 4. 推荐版式

默认采用简洁导读版式：

- 一级标题：节目名_导读
- 正文开头：日期 / 来源链接（如有）
- 二级标题：关键词 / 全文摘要 / 章节速览 / 核心观点 / 商业启发 / 待核实点
- 正文段落：正常段落，不做过度花哨排版

## 5. 默认文件名

- `节目名_导读.docx`
- 如果有 Vol 编号：`Vol.xxx 节目名_导读.docx`

## 6. 与 docx 能力的衔接

推荐动作：

- 先整理 Markdown 结构稿
- 再优先使用 `scripts/export_docx.py`
- 如果用户有更复杂版式要求，再考虑额外 docx 能力

如果环境缺少可靠 docx 导出链路：
- 先交 Markdown 成稿
- 明确说明“docx 导出链路当前不可用”

## 7. 示例

```bash
python3 scripts/export_docx.py ./output/春秋航空_导读.md -o ./output/春秋航空_导读.docx
```

## 8. 交付前检查

至少检查：

1. docx 标题是否正确
2. 各级标题是否完整
3. Markdown 与 docx 内容是否一致
4. 是否误把待核实内容写成确定事实
5. 链接来源是否需要写入文档开头
