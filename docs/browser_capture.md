# Browser Capture

这份文档定义：当播客页面需要 **JS 渲染、展开 transcript、滚动加载、点击“Show More”**，或者需要用户先登录时，`podcast_analysis_doc` 应如何借助浏览器能力继续抓取内容。

## 1. 什么时候应该从 requests 切到浏览器

如果出现以下任一情况，不要只靠 `scripts/fetch_podcast_page.py`：

- 页面正文是前端渲染，requests 抓到的只有壳
- transcript 默认折叠，需要点击展开
- 页面要滚动到底部才继续加载正文
- 页面需要登录后才能看到完整内容
- 页面里存在“Transcript / 显示全文 / 展开更多 / Show More / Read More / Captions”之类入口

这时应切到浏览器流程。

## 2. 默认浏览器流程

### A. 无需登录时
1. 用 `browser_use` 打开页面
2. `snapshot` 看结构
3. 找 transcript / show notes / expand 按钮
4. 必要时点击、滚动、等待加载
5. 再 `snapshot` 或 `evaluate` 提取正文
6. 判断内容级别：
   - `transcript_like`
   - `show_notes_like`
   - `summary_like`

### B. 需要登录时
1. 如果用户明确想看真实浏览器窗口，使用 `browser_visible` 的思路启动可见浏览器
2. 打开页面
3. 告知用户先完成登录
4. 登录完成后再继续 `snapshot / click / evaluate`
5. 只有确认正文可见后，才进入导读生成

## 3. 浏览器流程的目标

浏览器不是为了“多走一步流程”，而是为了解决：

- `requests` 看不到真实正文
- transcript 被折叠
- 页面需要人工参与

目标仍然只有一个：**拿到足够可靠的可分析文本**。

## 4. 优先查找哪些元素

优先关注这些文字或按钮：

- Transcript
- Show transcript
- Captions
- 展开全文
- 显示更多
- Read more
- Show more
- Episode notes
- Show notes
- 章节
- 全文

## 5. 提取后如何判断内容级别

### transcript_like
满足任一特征：
- 有连续正文，长度明显较长
- 有大量发言内容或逐段转录
- 有较多时间戳和对应段落

### show_notes_like
满足任一特征：
- 有章节标题、少量摘要、时间戳
- 有节目提纲，但没有连续逐字正文

### summary_like
满足任一特征：
- 只有节目简介、推荐文案、少量卡片信息
- 没有可支撑完整章节导读的正文

## 6. 页面需要用户介入时怎么说

推荐说法：

- “这个页面需要登录后才能看到完整 transcript。我可以先打开可见浏览器，你登录完成后我继续抓取正文。”
- “页面正文目前是折叠状态，我先尝试展开 transcript；如果需要你手动确认登录，我会停下来等你。”

## 7. 风险控制

绝对不要：

- 页面还没展开正文，就假装已经拿到 transcript
- 用户尚未登录成功，就继续声称可以完成完整导读
- 只拿到前几屏片段，就伪装成全量 transcript 分析

## 8. 推荐输出记录

完成浏览器抓取后，至少在内部判断里记录：

- 链接地址
- 是否使用浏览器抓取
- 是否需要登录
- 最终拿到的是 transcript / show notes / summary 哪一级
- 是否仍有正文缺口
