---
name: skillupload
description: 将指定的文件夹程序打包成 Gemini CLI Skill 并自动推送到用户的 GitHub 仓库。
---
# Skill 自动打包上传指南
当此 Skill 激活时，Agent 将按照以下步骤操作：

1. **GitHub 授权检查**：
   - 检查本地是否配置了 `GITHUB_TOKEN`。
   - 如果未配置，请运行 `python3 scripts/auth.py` 引导用户登录或输入个人访问令牌 (PAT)。

2. **代码整理与打包**：
   - 将 `upload/` 文件夹下或指定的程序目录整理为标准的 Skill 格式（包含 `SKILL.md`）。
   - 如果源文件夹没有 `SKILL.md`，Agent 会基于项目内容生成一个基础模板。

3. **Git 初始化与推送**：
   - 在该文件夹中初始化 Git 仓库。
   - 调用 `python3 scripts/uploader.py` 在 GitHub 上创建新仓库并将代码推送上去。

# 常用命令
- `python3 scripts/auth.py`: 进行 GitHub 登录/授权。
- `python3 scripts/uploader.py --path <folder_path> --repo <repo_name>`: 上传指定文件夹到指定仓库。
