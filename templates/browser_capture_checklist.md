# Browser Capture Checklist

当链接页通过普通抓取拿不到足够正文时，按这份清单检查：

- [ ] 已先尝试 `scripts/fetch_podcast_page.py`
- [ ] 已确认 requests 抓不到足够正文
- [ ] 已检查页面是否存在 transcript / show notes / 展开全文入口
- [ ] 已判断页面是否需要登录
- [ ] 若需要登录，已明确告知用户并等待其完成
- [ ] 已在浏览器中展开 transcript / show notes / 更多内容
- [ ] 已再次抓取或 snapshot 页面正文
- [ ] 已判断最终内容级别：`transcript_like / show_notes_like / summary_like`
- [ ] 若仍不足，已明确缺口，不硬写完整导读
