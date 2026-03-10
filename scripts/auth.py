import os
import sys
import webbrowser
import urllib.parse
from pathlib import Path

ENV_FILE = Path(__file__).parent.parent / ".env"

def main():
    print("=== GitHub 授权跳转 ===")
    
    # 预填权限：repo (读写仓库), workflow (更新 action), gist
    params = {
        "scopes": "repo,workflow,gist",
        "description": "Gemini_CLI_SkillUpload_Token",
    }
    auth_url = f"https://github.com/settings/tokens/new?{urllib.parse.urlencode(params)}"
    
    print("\n1. 正在为您在浏览器中打开 GitHub 授权页面...")
    print("2. 请在页面底部点击 'Generate token'。")
    print("3. 复制生成的令牌 (ghp_...) 并粘贴到下方。\n")
    
    try:
        webbrowser.open(auth_url)
    except Exception as e:
        print(f"无法自动打开浏览器，请手动访问：\n{auth_url}")

    token = input("请输入您的 GitHub Token: ").strip()
    
    if token.startswith("ghp_") or token.startswith("github_pat_"):
        with open(ENV_FILE, "w") as f:
            f.write(f"GITHUB_TOKEN={token}\n")
        print(f"\n✅ 授权成功！配置已保存到 {ENV_FILE}")
    else:
        print("\n❌ 令牌格式似乎不对，请确保是以 ghp_ 开头的字符串。")

if __name__ == "__main__":
    main()
