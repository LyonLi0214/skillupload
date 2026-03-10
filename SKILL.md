---
name: skillupload
description: 将指定的文件夹程序打包成 Gemini CLI Skill 并自动推送到用户的 GitHub 仓库。
---
# Skill 自动打包上传指南
当此 Skill 激活时，Agent 将按照以下步骤操作：

1. **环境初始化 (可选)**：
   - 如果用户首次使用，请运行 `python3 scripts/setup.py` 完成依赖安装、GitHub 授权以及本地链接。

2. **GitHub 授权检查**：
   - 检查本地是否配置了 `GITHUB_TOKEN`。
   - 如果未配置，请运行 `python3 scripts/auth.py`。

3. **代码整理与打包**：
   - 运行 `python3 scripts/packager.py --path <folder_path>` 整理文件夹并生成 `SKILL.md`。

4. **Git 推送**：
   - 调用 `python3 scripts/uploader.py --path <folder_path> --repo <repo_name>` 将项目推送到 GitHub。

# 常用命令
- `python3 scripts/setup.py`: 一键配置环境、授权并链接 Skill。
- `python3 scripts/auth.py`: 重新授权 GitHub。
- `python3 scripts/uploader.py --path <folder_path> --repo <repo_name>`: 上传指定项目。
