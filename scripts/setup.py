import os
import subprocess
import sys
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def run_command(command, description):
    print(f"\n🚀 正在执行: {description}...")
    result = subprocess.run(command, shell=True, cwd=BASE_DIR)
    return result.returncode == 0

def main():
    print("=== 通用 CLI 项目自动配置程序 ===")

    # 1. 基础环境检查
    run_command(f"{sys.executable} -m pip install -r requirements.txt", "安装 Python 核心依赖")

    # 2. 授权检查
    auth_script = BASE_DIR / "scripts" / "auth.py"
    run_command(f"{sys.executable} {auth_script}", "GitHub 身份验证")

    # 3. 自动识别并链接到 AI CLI 环境
    print("\n🔍 正在探测系统中的 AI CLI 环境...")
    
    linked = False
    # 探测 Gemini CLI
    if shutil.which("gemini"):
        print("发现 [Gemini CLI]，正在自动链接...")
        if run_command(f"gemini skills link {BASE_DIR}", "链接到 Gemini CLI"):
            linked = True

    # 探测 MCP (Model Context Protocol) 或其他 AI CLI 可以在此扩展
    # if shutil.which("mcp"): ...

    if not linked:
        print("\n⚠️ 未检测到已知的 AI CLI。您可以将此项目作为独立 Python 工具使用。")
    else:
        print("\n✅ 已自动链接至您的 CLI 环境。")

    print("\n🎉 配置完成！")

if __name__ == "__main__":
    main()
