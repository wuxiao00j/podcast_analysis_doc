# 示例：通过浏览器展开 transcript，再生成导读

## 场景

用户给了一个播客链接，但：
- 普通请求只能抓到简介
- transcript 在页面里默认折叠
- 页面可能还需要登录

## 正确动作顺序

1. 先跑 `scripts/fetch_podcast_page.py`
2. 判断结果若偏 `summary_like`，不要急着放弃
3. 进入 `docs/browser_capture.md`
4. 用浏览器打开页面
5. 查找 transcript / Show More / 展开全文
6. 如果页面要求登录：
   - 提醒用户先登录
   - 登录后继续抓取
7. 正文拿到后，再判断：
   - 能否写完整导读
   - 还是只能写轻量版
8. 如果用户要求 `.docx`：
   - 先出 Markdown
   - 再导出 `.docx`

## 这个示例的重点

- `requests` 不够，不代表任务失败
- 浏览器增强流程是为了拿到更完整正文
- 但即使用了浏览器，也不能在正文不足时硬写完整章节导读
