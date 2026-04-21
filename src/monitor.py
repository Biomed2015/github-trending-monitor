#!/usr/bin/env python3
"""
GitHub Top 20 高 Star 仓库每日监控脚本
定时获取 GitHub 排名前 20 的高 star 仓库，格式化输出到终端
"""

import os
import sys
import requests
from datetime import datetime

GITHUB_API = "https://api.github.com/search/repositories"
QUERY = "stars:>10000"
SORT = "stars"
ORDER = "desc"
PER_PAGE = 20


def fetch_top_repos(token=None, per_page=PER_PAGE):
    """获取 GitHub top 仓库"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    params = {
        "q": QUERY,
        "sort": SORT,
        "order": ORDER,
        "per_page": per_page,
    }

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在获取 GitHub Top {per_page} 高 Star 仓库...")
    print("=" * 80)

    try:
        resp = requests.get(GITHUB_API, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("items", [])
    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)


def format_stars(stars):
    """格式化 star 数量"""
    if stars >= 1000:
        return f"{stars / 1000:.1f}k"
    return str(stars)


def print_repos(repos):
    """格式化打印仓库列表"""
    print(f"\n{'=' * 80}")
    print(f"  📦 GitHub Top {len(repos)} 高 Star 仓库排行榜")
    print(f"  🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)")
    print(f"{'=' * 80}\n")

    # 表头
    print(f"  {'排名':<4} {'仓库名称':<35} {'⭐ Stars':<8} {'语言':<10} {'描述'}")
    print(f"  {'-' * 4} {'-' * 35} {'-' * 8} {'-' * 10} {'-' * 40}")

    for i, repo in enumerate(repos, 1):
        name = repo.get("full_name", "")
        stars = repo.get("stargazers_count", 0)
        language = repo.get("language") or "Unknown"
        description = repo.get("description") or "无描述"
        url = repo.get("html_url", "")

        # 截断过长的描述
        if len(description) > 40:
            description = description[:37] + "..."

        # 截断过长的仓库名
        if len(name) > 35:
            name = name[:32] + "..."

        stars_str = format_stars(stars)
        print(f"  {i:<4} {name:<35} {stars_str:<8} {language:<10} {description}")

        # 打印 URL（小字）
        print(f"       🔗 {url}")
        print()

    print(f"{'=' * 80}")
    print(f"  📌 共监控 {len(repos)} 个仓库，快去看看有没有适合你的应用吧！")
    print(f"{'=' * 80}\n")


def main():
    token = os.environ.get("GITHUB_TOKEN")
    repos = fetch_top_repos(token=token)
    print_repos(repos)

    if not repos:
        print("⚠️ 未能获取到任何仓库信息")
        sys.exit(1)

    print("✅ 监控任务执行完成")


if __name__ == "__main__":
    main()
