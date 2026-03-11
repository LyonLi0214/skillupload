# 🚀 Gemini Skill Upload (skillupload)

`skillupload` 是一个专为 **Gemini CLI** 设计的自动化工具（Skill）。它可以帮助开发者一键将本地的 Python 脚本或工作流整理成标准的 Gemini Skill 格式，并自动推送到 GitHub 仓库。

## ✨ 功能特性

*   **一键配置**：提供 `setup.py` 脚本，自动安装依赖、跳转授权并链接本地 Skill。
*   **智能打包**：自动为项目生成 `SKILL.md` 模板（如果缺失），确保符合 Gemini CLI 标准。
*   **GitHub 自动化**：自动在您的 GitHub 账户下创建远程仓库并推送代码。
*   **安全保护**：内置 `.gitignore`，自动过滤 `.env` 令牌文件，防止敏感信息泄露。

## 🛠️ 安装与配置

### 1. 克隆项目
```bash
git clone https://github.com/LyonLi0214/skillupload.git
cd skillupload
```

### 2. 运行自动化配置
```bash
python3 scripts/setup.py
```
*   **步骤提示**：
    1.  脚本会安装 `PyGithub` 等必要依赖。
    2.  会自动打开浏览器跳转至 GitHub 授权页，请生成并复制 Token。
    3.  将 Token 粘贴回终端。
    4.  脚本会自动运行 `gemini skills link` 将此工具注册到您的 Gemini CLI 中。

## 📖 使用指南

在您的 Gemini CLI 对话框中，您可以直接下达指令：

### 场景 A：打包上传 upload 文件夹里的项目
1. 将您的项目文件夹放入 `skillupload/upload/` 目录下。
2. 对 Gemini 说：
   > “帮我把 upload 里的 [文件夹名] 打包上传到 GitHub。”

### 场景 B：上传任意路径的文件夹
> “激活 skillupload，将路径为 /Users/xxx/my-project 的项目上传到名为 my-new-skill 的 GitHub 仓库。”

## 📁 项目结构
```text
skillupload/
├── SKILL.md           # Gemini Skill 核心描述文件
├── README.md          # 项目文档
├── requirements.txt   # Python 依赖清单
├── scripts/
│   ├── setup.py       # 一键安装与链接脚本
│   ├── auth.py        # GitHub 授权跳转逻辑
│   ├── packager.py    # 智能生成 SKILL.md
│   └── uploader.py    # GitHub API 与 Git 推送逻辑
└── upload/            # 待上传项目的暂存区
```

## ⚠️ 安全说明
*   您的 GitHub Token 保存在本地的 `.env` 文件中。
*   项目已配置 `.gitignore`，**永远不会**将您的 Token 推送到公共仓库。
*   建议定期更换您的 Personal Access Token。

---
*Powered by Gemini CLI*
