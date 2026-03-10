import os
import sys
import argparse
from pathlib import Path
from github import Github, GithubException
from dotenv import load_dotenv
import subprocess

# 加载 .env 中的 GITHUB_TOKEN
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def run_git_command(command, cwd):
    print(f"执行命令: {' '.join(command)}")
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 命令失败: {result.stderr}")
        return False
    return True

def main(args):
    if not GITHUB_TOKEN:
        print("❌ 错误：未找到 GITHUB_TOKEN，请运行 scripts/auth.py 配置。")
        sys.exit(1)

    path = Path(args.path).resolve()
    if not path.exists():
        print(f"❌ 路径不存在: {path}")
        sys.exit(1)

    repo_name = args.repo or path.name
    
    # 1. 登录 GitHub
    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    print(f"👤 已登录为: {user.login}")

    # 2. 创建仓库 (如果不存在)
    try:
        repo = user.get_repo(repo_name)
        print(f"📂 仓库 {repo_name} 已存在")
    except GithubException:
        print(f"🚀 正在创建仓库: {repo_name}...")
        repo = user.create_repo(repo_name, private=False)

    # 3. 本地 Git 推送
    # 初始化
    if not (path / ".git").exists():
        run_git_command(["git", "init"], path)
    
    # 添加远程仓库 (如果已存在则更新)
    remote_url = f"https://{GITHUB_TOKEN}@github.com/{user.login}/{repo_name}.git"
    run_git_command(["git", "remote", "remove", "origin"], path)
    run_git_command(["git", "remote", "add", "origin", remote_url], path)

    # 提交并推送
    run_git_command(["git", "add", "."], path)
    run_git_command(["git", "commit", "-m", "Initial commit from skillupload"], path)
    run_git_command(["git", "branch", "-M", "main"], path)
    
    print(f"📤 正在推送到 GitHub...")
    if run_git_command(["git", "push", "-u", "origin", "main", "--force"], path):
        print(f"✅ 成功！项目已上传至: {repo.html_url}")
    else:
        print("❌ 推送失败。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="要上传的文件夹路径")
    parser.add_argument("--repo", help="GitHub 仓库名称 (可选)")
    args = parser.parse_args()
    main(args)
