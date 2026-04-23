# Other Agent Quickstart

这份文档给“准备把 `podcast_analysis_doc` 装给其他 agent”的人看。

## 1. skill 路径

把整个目录提供给目标 agent：

```text
/Users/barry/Desktop/cursor/skill/skills/podcast_analysis_doc
```

## 2. 推荐让对方先读什么

最短阅读顺序：

1. `SKILL.md`
2. `docs/workflow.md`
3. `docs/link_handling.md`
4. `docs/browser_capture.md`
5. `docs/docx_export.md`
6. `examples/chunqiu_airlines_example.md`
7. `examples/podcast_link_to_docx_example.md`

## 3. 你可以直接给对方的任务话术

### 话术 A：完整链路

> 用 `podcast_analysis_doc` 处理这个播客链接。先判断页面有没有 transcript；如果信息足够，先生成 Markdown 导读，再导出 `.docx`。如果信息不足，就明确告诉我缺什么，不要硬写完整章节导读。

### 话术 B：对齐风格

> 按 `examples/chunqiu_airlines_example.md` 的风格，给这期播客生成导读 `.docx`。

### 话术 C：安全兜底

> 如果当前链接页只有简介或 show notes，没有 transcript，请先停在“轻量版导读”或向我要 transcript，不要编造时间戳和完整章节内容。

### 话术 D：浏览器增强

> 如果 requests 抓不到正文，或者 transcript 需要点击展开 / 登录后可见，请切到浏览器增强抓取，不要直接判定无法完成。

## 4. 目标 agent 应优先用哪些文件

### 抓链接判断质量
- `scripts/fetch_podcast_page.py`
- `docs/link_handling.md`

### 浏览器增强抓取
- `docs/browser_capture.md`
- `templates/browser_capture_checklist.md`
- `templates/browser_login_pause_message.md`

### 写导读结构稿
- `templates/podcast_analysis_template.md`
- `templates/enhanced_analysis_template.md`
- `docs/writing_guide.md`

### 导出 Word
- `scripts/export_docx.py`
- `docs/docx_export.md`
- `templates/docx_delivery_checklist.md`

## 5. 当前这套 skill 的真实能力边界

已经能做：
- 链接页质量粗判
- requests 抓取不到正文时切换浏览器增强流程
- 结构化 Markdown 导读
- macOS 下把 Markdown 导出成简洁 `.docx`

还不保证：
- 自动拿到所有平台的隐藏 transcript
- 复杂排版的 Word 成品
- 音频文件本地自动转录

## 6. 最后提醒

让别的 agent 使用时，最重要的不是“会不会写摘要”，而是：

- 会不会先判断链接质量
- 会不会在 transcript 不足时停下来
- 会不会在需要时切到浏览器增强抓取
- 会不会先出 Markdown 再出 docx

这几件事比文风更重要。
