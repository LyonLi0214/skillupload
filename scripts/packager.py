import os
import sys
from pathlib import Path

def identify_project(folder_path):
    print(f"🔍 正在智能识别项目类型: {folder_path.name}")
    
    files = [f.name for f in folder_path.iterdir() if f.is_file()]
    
    # 识别逻辑
    if "package.json" in files:
        return "Node.js (NPM)"
    elif "requirements.txt" in files or any(folder_path.glob("*.py")):
        return "Python"
    elif "go.mod" in files:
        return "Go"
    return "通用代码项目"

def generate_metadata(folder_path, name):
    project_type = identify_project(folder_path)
    print(f"✅ 项目类型识别为: {project_type}")

    skill_md_path = folder_path / "SKILL.md"
    if not skill_md_path.exists():
        print(f"🚀 为 AI Agent 自动生成 Skill 元数据...")
        content = f"""---
name: {name.lower().replace(' ', '-')}
description: 此项目是一个 {project_type} 自动化工具，由 skillupload 自动上传。
---
# {name} 使用指南
此项目类型为：{project_type}。
在使用此 Skill 之前，请确保已安装相应的环境并配置好依赖。
"""
        with open(skill_md_path, "w") as f:
            f.write(content)
        print(f"✅ 已生成 Skill 描述文件。")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    if target_path.exists():
        generate_metadata(target_path, target_path.name)

if __name__ == "__main__":
    main()
