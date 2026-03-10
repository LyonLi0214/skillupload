import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def run_command(command, description):
    print(f"\n🚀 正在执行: {description}...")
    result = subprocess.run(command, shell=True, cwd=BASE_DIR)
    if result.returncode != 0:
        print(f"❌ {description} 失败。")
        return False
    print(f"✅ {description} 成功。")
    return True

def main():
    print("=== skillupload 自动配置程序 ===")

    # 1. 安装依赖
    run_command(f"{sys.executable} -m pip install -r requirements.txt", "安装 Python 依赖")

    # 2. 授权跳转
    auth_script = BASE_DIR / "scripts" / "auth.py"
    run_command(f"{sys.executable} {auth_script}", "配置 GitHub 授权")

    # 3. 链接 Skill 到 Gemini CLI
    # 使用 absolute path 确保链接正确
    run_command(f"gemini skills link {BASE_DIR}", "链接 Skill 到 Gemini CLI")

    print("\n🎉 所有配置已完成！您现在可以开始使用 skillupload 了。")

if __name__ == "__main__":
    main()
