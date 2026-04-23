# 示例：用户只给播客链接，要求导出导读 docx

## 用户请求

> 给你一个播客链接，按春秋航空那篇的风格，帮我生成导读 docx。

## 正确动作顺序

1. 先进入 `podcast_analysis_doc`
2. 读取：
   - `docs/workflow.md`
   - `docs/link_handling.md`
   - `docs/docx_export.md`
3. 打开链接页面
4. 先判断页面是否有：
   - 标题
   - 日期
   - show notes
   - 时间戳
   - transcript
5. 如果 transcript 足够：
   - 生成 Markdown 导读稿
   - 再导出 `.docx`
6. 如果只有简介 / show notes：
   - 明确说明只能先做轻量版导读
   - 或向用户补要转录稿

## 不该做什么

- 不该只看节目简介就伪装成完整章节导读
- 不该编造时间戳
- 不该直接跳过 Markdown 中间稿

## 推荐对用户的最小确认

如果页面内容不足，可这样问：

> 这个链接页目前没有完整 transcript。你要我先基于 show notes 做一个轻量版导读 docx，还是你补转录稿，我再给你做完整版？
