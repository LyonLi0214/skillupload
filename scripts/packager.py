import os
import sys
import argparse
from pathlib import Path

def generate_skill_md(folder_path, name):
    skill_md_path = folder_path / "SKILL.md"
    if skill_md_path.exists():
        print(f"✅ {name} 文件夹已有 SKILL.md，跳过生成。")
        return

    print(f"🚀 正在为 {name} 生成基础 SKILL.md...")
    
    # 简单的自动分析：是否有 python 文件？
    has_python = any(folder_path.glob("**/*.py"))
    
    content = f"""---
name: {name.lower().replace(' ', '-')}
description: 此 Skill 自动打包自 {name}。请根据脚本内容调整此描述。
---
# {name} Skill 指南
当此 Skill 激活时：
1. **环境准备**：检查是否有 requirements.txt 并安装。
2. **执行指令**：根据项目结构运行主要入口程序。
"""
    with open(skill_md_path, "w") as f:
        f.write(content)
    print(f"✅ 已生成 {skill_md_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="待整理的文件夹路径")
    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    if not target_path.exists() or not target_path.is_dir():
        print(f"❌ 路径无效: {target_path}")
        sys.exit(1)

    generate_skill_md(target_path, target_path.name)

if __name__ == "__main__":
    main()
