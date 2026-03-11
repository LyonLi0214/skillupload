#!/usr/bin/env python3
"""
skillupload — 读取 SKILL.md，生成 GitHub README，推送到 GitHub。

用法:
    python3 upload.py --path <项目文件夹> [--repo <仓库名>] [--private]
"""

import os
import sys
import argparse
import re
import subprocess
from pathlib import Path
from github import Github, GithubException
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# ─── 1. 读取并解析 SKILL.md ───────────────────────────────────────────────────

def parse_skill_md(skill_md_path: Path) -> dict:
    """从 SKILL.md 提取 frontmatter 和正文内容。"""
    text = skill_md_path.read_text(encoding="utf-8")

    # 提取 YAML frontmatter
    meta = {"name": "", "description": ""}
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if frontmatter_match:
        fm = frontmatter_match.group(1)
        for line in fm.splitlines():
            if line.startswith("name:"):
                meta["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("description:"):
                meta["description"] = line.split(":", 1)[1].strip()

    # 正文（frontmatter 之后的内容）
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL).strip()

    return {"name": meta["name"], "description": meta["description"], "body": body, "raw": text}


# ─── 2. 生成 GitHub README.md ─────────────────────────────────────────────────

def generate_readme(skill: dict, repo_url: str) -> str:
    """从 SKILL.md 内容生成 GitHub README.md。"""
    name = skill["name"] or "skill"
    description = skill["description"]
    body = skill["body"]

    # 提取"使用方式"部分的代码块，作为 README 的快速开始
    quick_start = ""
    code_blocks = re.findall(r"```(?:bash|sh)?\n(.*?)```", body, re.DOTALL)
    if code_blocks:
        first_cmd = code_blocks[0].strip().splitlines()[0]
        quick_start = f"\n## Quick Start\n\n```bash\n{first_cmd}\n```\n"

    readme = f"""# {name}

> {description}

[![GitHub](https://img.shields.io/badge/GitHub-{name}-blue)](https://github.com/{repo_url})
{quick_start}
---

{body}

---

> 本项目由 [skillupload](https://github.com/LyonLi0214/skillupload) 自动发布。
"""
    return readme


# ─── 3. 推送到 GitHub ─────────────────────────────────────────────────────────

def run_git(command: list, cwd: Path) -> bool:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ {' '.join(command)}\n     {result.stderr.strip()}")
    return result.returncode == 0


def push_to_github(project_path: Path, repo_name: str, readme_content: str, private: bool):
    """写入 README，初始化 git，推送到 GitHub。"""
    if not GITHUB_TOKEN:
        print("❌ 未找到 GITHUB_TOKEN，请在 .env 文件中配置：GITHUB_TOKEN=ghp_xxx")
        sys.exit(1)

    # 写入 README
    readme_path = project_path / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"  ✅ README.md 已生成 ({len(readme_content)} 字符)")

    # GitHub API
    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    print(f"  👤 GitHub 用户: {user.login}")

    try:
        repo = user.get_repo(repo_name)
        print(f"  📂 仓库已存在: {repo.html_url}")
    except GithubException:
        print(f"  🚀 创建仓库: {repo_name}...")
        repo = user.create_repo(repo_name, private=private, auto_init=False)

    # Git 操作
    remote_url = f"https://{GITHUB_TOKEN}@github.com/{user.login}/{repo_name}.git"
    if not (project_path / ".git").exists():
        run_git(["git", "init"], project_path)
    run_git(["git", "remote", "remove", "origin"], project_path)
    run_git(["git", "remote", "add", "origin", remote_url], project_path)
    run_git(["git", "add", "."], project_path)
    run_git(["git", "commit", "-m", f"Update: {repo_name}"], project_path)
    run_git(["git", "branch", "-M", "main"], project_path)

    print(f"  📤 推送中...")
    if run_git(["git", "push", "-u", "origin", "main", "--force"], project_path):
        print(f"\n✅ 完成！仓库地址: {repo.html_url}")
        return repo.html_url
    else:
        print("❌ 推送失败")
        return None


# ─── 4. 主流程 ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="读取 SKILL.md → 生成 README → 推送 GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python3 upload.py --path ~/my-app/tt-live-analysis
  python3 upload.py --path ~/my-app/my-tool --repo my-tool --private
""")
    parser.add_argument("--path", required=True, help="项目文件夹路径（必须含 SKILL.md）")
    parser.add_argument("--repo", help="GitHub 仓库名称（默认：文件夹名）")
    parser.add_argument("--private", action="store_true", help="创建私有仓库")
    args = parser.parse_args()

    project_path = Path(args.path).resolve()
    if not project_path.exists():
        print(f"❌ 路径不存在: {project_path}")
        sys.exit(1)

    skill_md_path = project_path / "SKILL.md"
    if not skill_md_path.exists():
        print(f"❌ 未找到 SKILL.md: {skill_md_path}")
        print("   请先在项目文件夹中创建 SKILL.md，或使用 universal-skill-maker 生成。")
        sys.exit(1)

    repo_name = args.repo or project_path.name
    print(f"\n📦 处理项目: {project_path.name}")
    print(f"   → GitHub 仓库: {repo_name}\n")

    # 解析 SKILL.md
    print("1. 读取 SKILL.md...")
    skill = parse_skill_md(skill_md_path)
    print(f"   name: {skill['name']}")
    print(f"   description: {skill['description'][:60]}...")

    # 生成 README
    print("\n2. 生成 README.md...")
    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    readme = generate_readme(skill, f"{user.login}/{repo_name}")

    # 推送
    print("\n3. 推送到 GitHub...")
    push_to_github(project_path, repo_name, readme, args.private)


if __name__ == "__main__":
    main()
