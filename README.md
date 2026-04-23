# podcast_analysis_doc

`podcast_analysis_doc` 是一个把播客链接、转录稿、`.docx`、文本稿等材料整理成结构化导读文档的 skill。

它的目标不是只做摘要，而是产出可交付的导读稿；在用户要求时，还要继续导出成 `.docx`。

## 适用场景

- 把一段播客转录稿整理成导读
- 给一个播客链接，自动抓节目页信息并判断是否能生成完整导读
- 把商业类节目做成“关键词 + 摘要 + 章节速览”文档
- 把访谈节目沉淀成内部知识库条目
- 把内容运营素材加工成可发布的长文底稿
- 最终输出 Word 版导读文档

## 正文来源优先级

写导读时，正文依据默认按以下顺序取用：

1. 用户提供的转录稿 / 字幕 / 音频转写结果
2. 音频文件转录得到的正文
3. 页面内完整 transcript
4. show notes / 章节提纲
5. 页面标题、简介、meta description

原则：
- 如果用户给了音频或转录稿，**不要只根据页面信息写正文**
- 页面信息主要用于补标题、日期、嘉宾、来源链接
- 页面信息也可用于判断“是否还缺完整 transcript”
- 没有正文时，最多输出轻量版导读，不要伪装成完整版

## 仓库结构

```text
podcast_analysis_doc/
├── SKILL.md
├── README.md
├── docs/
│   ├── workflow.md
│   ├── source_handling.md
│   ├── link_handling.md
│   ├── browser_capture.md
│   ├── writing_guide.md
│   ├── docx_export.md
│   ├── other_agent_quickstart.md
│   └── runtime_requirements.md
├── scripts/
│   ├── fetch_podcast_page.py
│   ├── export_docx.py
│   └── smoke_test.py
├── templates/
│   ├── podcast_analysis_template.md
│   ├── enhanced_analysis_template.md
│   ├── docx_delivery_checklist.md
│   ├── link_input_prompt.txt
│   ├── agent_handoff_prompt.txt
│   ├── browser_capture_checklist.md
│   ├── browser_login_pause_message.md
│   └── transcript_missing_response.md
└── examples/
    ├── chunqiu_airlines_example.md
    ├── chunqiu_airlines_example.docx
    ├── podcast_link_to_docx_example.md
    └── browser_transcript_capture_example.md
```

## 默认流程

1. 识别输入类型
2. 提取或抓取可读文本
3. 识别节目基础信息
4. 提炼主线论点
5. 按时间戳或主题切段
6. 写成结构化导读文档
7. 如用户要求，再导出成 `.docx`

## 三段式抓取思路

### 第一层：普通抓取
先用 `scripts/fetch_podcast_page.py` 粗判页面。

### 第二层：浏览器增强抓取
如果页面需要 JS 渲染、展开 transcript、滚动加载或登录，再进入 `docs/browser_capture.md`。

### 第三层：文档导出
内容足够后，先写 Markdown，再用 `scripts/export_docx.py` 导出 `.docx`。

## 当前内置脚本

### `scripts/fetch_podcast_page.py`
作用：
- 抓播客页面
- 粗判内容级别：`transcript_like / show_notes_like / summary_like`
- 帮 agent 决定能不能写完整导读

### `scripts/export_docx.py`
作用：
- 把 Markdown 导读稿转成简单 `.docx`
- 当前走 macOS `textutil` 链路
- 适合标题、段落、列表这种轻文档结构

### `scripts/smoke_test.py`
作用：
- 快速检测当前环境能否跑通最小闭环
- 包括链接抓取测试和 docx 导出测试

## 给其他 agent 的最短使用说明

如果你把这个 skill 装给别的 agent，可以直接这样下指令：

- “用 `podcast_analysis_doc` 分析这个播客链接，先判断页面有没有 transcript；如果信息足够，生成导读 Markdown，再导出成 docx。”
- “按 `examples/chunqiu_airlines_example.md` 的风格，给这期播客生成导读 docx。”
- “如果链接页只有 show notes、没有 transcript，就先告诉我缺什么，不要硬写完整章节导读。”
- “如果 requests 抓不到正文，就切到浏览器增强抓取，不要过早下结论。”

## 输出模式

### 标准版
- 标题
- 日期 / 来源
- 关键词
- 全文摘要
- 章节速览

### 增强版
在标准版上增加：
- 核心观点
- 商业启发
- 待核实点
- 可验证数据点

### Word 交付版
在标准版或增强版基础上，导出 `.docx`。

## 质量原则

- 不编造时间戳
- 不编造数据
- 不把主播闲聊当核心论点
- 不只做流水账复述
- 区分“节目原话”和“你的分析判断”
- 信息不足时明确说明边界
- 只有链接简介时，不伪装成完整转录级导读
- 页面需要登录或展开正文时，要明确切换到浏览器增强流程
