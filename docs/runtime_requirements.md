# Runtime Requirements

这份文档说明 `podcast_analysis_doc` 在不同环节依赖什么。

## 1. 最低可用要求

想让这个 skill 至少能“判断链接质量 + 生成 Markdown 导读”，最低要求是：

- `python3`
- Python `requests`
- 能读取本地文本文件 / 网页内容

## 2. macOS 下的推荐最小可交付环境

如果你希望它还能导出 `.docx`，推荐满足：

- `python3`
- Python `requests`
- 系统自带 `textutil`

这套组合已经足够跑通：

- `scripts/fetch_podcast_page.py`
- `scripts/export_docx.py`

## 3. 当前内置脚本各自依赖

### `scripts/fetch_podcast_page.py`
依赖：
- Python 标准库
- `requests`

用途：
- 拉取播客页面
- 提取标题、meta、正文摘录
- 粗判页面内容级别

### `scripts/export_docx.py`
依赖：
- Python 标准库
- macOS `textutil`

用途：
- 把 Markdown 结构稿转成简洁 `.docx`

## 4. 不依赖的东西

当前这版 skill **不要求**：

- `pandoc`
- `node`
- `npm`
- `python-docx`
- `LibreOffice`

这些东西以后可以增强，但不是当前最小闭环的必需项。

## 5. 当前能力边界

即使依赖都满足，也仍然要注意：

- 并不是所有播客平台页面都公开 transcript
- 需要登录、展开、滚动加载的 transcript，不一定能靠简单抓取拿到
- 当前导出的 `.docx` 是简洁版导读，不是复杂排版文档

## 6. 推荐自检顺序

把 skill 装给别的 agent 后，建议先做这几个检查：

1. 能否读取 `SKILL.md`
2. 能否运行：
   ```bash
   python3 scripts/fetch_podcast_page.py --url 'https://example.com'
   ```
3. 能否运行：
   ```bash
   python3 scripts/export_docx.py examples/chunqiu_airlines_example.md -o /tmp/test.docx
   ```
4. 是否明确知道：没有 transcript 时应停下来补问
