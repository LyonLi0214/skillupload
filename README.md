# 🚀 CLI Project Upload (skillupload)

`skillupload` 是一个通用的 **CLI 项目自动化发布工具**。它可以自动识别您的 AI 运行环境（如 Gemini CLI 等），并一键将本地的各种项目（Python, Node.js 等）打包、生成 Skill 描述文件并发布到 GitHub。

## ✨ 通用功能特性

*   **自动识别环境**：`setup.py` 自动探测并链接至系统已安装的 AI CLI。
*   **智能项目分析**：`packager.py` 自动识别项目语言（Python, JS, Go 等）。
*   **一键 GitHub 发布**：自动化创建仓库、管理 Token 并完成推送。

## 🛠️ 安装与自动配置
```bash
git clone https://github.com/LyonLi0214/skillupload.git
cd skillupload
python3 scripts/setup.py
```
*运行 `setup.py` 后，它会自动将自己链接到所有已识别的 AI CLI 中。*
