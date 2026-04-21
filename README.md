# GitHub Top 20 高 Star 应用每日监控

每天定时获取 GitHub 排名前 20 的高 Star 仓库，通过 GitHub Actions 自动运行，邮件 + 终端双通道通知。

## 功能特性

- 每天 09:00 (北京时间) 自动获取 GitHub Top 20 高 Star 仓库
- 美化表格输出，直接在 Action 日志中查看
- 支持手动触发 (`workflow_dispatch`)
- 可选 SMTP 邮件通知

## 快速上手

### 1. Fork 本仓库

### 2. （可选）配置邮件通知

在仓库 `Settings > Secrets` 中添加：
- `SMTP_USER` — 发送邮箱
- `SMTP_PASS` — 邮箱密码/授权码

### 3. 查看 Actions 日志

每次 workflow 运行后，可在 `Actions` 标签页查看输出。

## 本地测试

```bash
pip install -r requirements.txt
GITHUB_TOKEN=your_token python src/monitor.py
```

> 不带 token 也能运行，但 GitHub API 速率限制会更严格。

## 定时说明

GitHub Actions 使用 UTC 时区：
- 北京时间 09:00 = UTC 1:00
- cron 表达式：`0 1 * * *`
