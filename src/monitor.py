#!/usr/bin/env python3
"""
GitHub Top 20 高 Star 单应用软件每日监控脚本
定时获取 GitHub 排名前 20 的高 star 单应用软件，格式化输出到终端
"""

import os
import sys
import requests
from datetime import datetime

GITHUB_API = "https://api.github.com/search/repositories"
# 搜索单应用软件：stars>10000，排除框架、库、模板、主题等项目类型
QUERY = "stars:>10000 NOT:framework NOT:library NOT:starter NOT:template NOT:theme NOT:boilerplate NOT:cli NOT:toolkit NOT:sdk"
SORT = "stars"
ORDER = "desc"
PER_PAGE = 30  # 获取更多以便过滤


def fetch_top_repos(token=None, per_page=PER_PAGE):
    """获取 GitHub top 单应用软件"""
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

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在获取 GitHub Top 单应用软件...")
    print("=" * 80)

    try:
        resp = requests.get(GITHUB_API, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("items", [])
    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)


def filter_single_apps(repos):
    """过滤出单应用软件，排除框架、库等"""
    exclude_keywords = [
        "framework", "library", "starter", "template", "theme",
        "boilerplate", "cli", "toolkit", "sdk", "plugin", "extension",
        "bundler", "packager", "generator", "scaffold", "seed",
        "bootstrap", "ui-kit", "component", "components", "icons",
        "icon-set", "design-system", "styleguide", "blocks",
        "-starter", "starter-", "example", "demo", "sample",
        "collection", "list", "awesome", "curated"
    ]

    filtered = []
    for repo in repos:
        name = repo.get("name", "").lower()
        full_name = repo.get("full_name", "").lower()
        description = repo.get("description", "").lower() if repo.get("description") else ""

        # 检查是否包含排除关键词
        is_excluded = False
        for keyword in exclude_keywords:
            if keyword in name or keyword in full_name or keyword in description:
                is_excluded = True
                break

        if not is_excluded:
            filtered.append(repo)

        if len(filtered) >= 20:
            break

    return filtered


def format_stars(stars):
    """格式化 star 数量"""
    if stars >= 1000:
        return f"{stars / 1000:.1f}k"
    return str(stars)


def print_repos(repos):
    """格式化打印软件列表"""
    print(f"\n{'=' * 80}")
    print(f"  📦 GitHub Top {len(repos)} 高 Star 单应用软件排行榜")
    print(f"  🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)")
    print(f"{'=' * 80}\n")

    # 表头
    print(f"  {'排名':<4} {'软件名称':<30} {'⭐ Stars':<8} {'语言':<10} {'描述'}")
    print(f"  {'-' * 4} {'-' * 30} {'-' * 8} {'-' * 10} {'-' * 45}")

    for i, repo in enumerate(repos, 1):
        name = repo.get("full_name", "")
        stars = repo.get("stargazers_count", 0)
        language = repo.get("language") or "Unknown"
        description = repo.get("description") or "无描述"
        url = repo.get("html_url", "")

        # 截断过长的描述
        if len(description) > 45:
            description = description[:42] + "..."

        # 截断过长的软件名
        if len(name) > 30:
            name = name[:27] + "..."

        stars_str = format_stars(stars)
        print(f"  {i:<4} {name:<30} {stars_str:<8} {language:<10} {description}")

        # 打印 URL（小字）
        print(f"       🔗 {url}")
        print()

    print(f"{'=' * 80}")
    print(f"  📌 共监控 {len(repos)} 款单应用软件，快去看看有没有适合你的吧！")
    print(f"{'=' * 80}\n")


def main():
    token = os.environ.get("GITHUB_TOKEN")
    all_repos = fetch_top_repos(token=token)
    repos = filter_single_apps(all_repos)
    print_repos(repos)

    if not repos:
        print("⚠️ 未能获取到任何软件信息")
        sys.exit(1)

    print("✅ 监控任务执行完成")


if __name__ == "__main__":
    main()
