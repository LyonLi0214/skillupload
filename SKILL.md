---
name: skillupload
description: 读取项目文件夹中的 SKILL.md，自动提取名称和描述，生成 GitHub README，并推送到 GitHub 仓库。项目文件夹必须已包含 SKILL.md 文件。
user-invocable: true
---

# skillupload — Skill 自动上传工具

当此 Skill 激活时，Agent 按以下步骤操作：

## 前置条件

- Python 3.9+
- 依赖：`pip3 install -r requirements.txt`（PyGithub, python-dotenv）
- 在 `/Users/lyon/my-app/skillupload/.env` 中配置 `GITHUB_TOKEN=ghp_xxx`
- 目标项目文件夹中必须已有 `SKILL.md` 文件（含 YAML frontmatter）

## 使用方式

### 基本用法
```bash
cd /Users/lyon/my-app/skillupload
python3 upload.py --path <项目文件夹路径>
```

### 指定仓库名
```bash
python3 upload.py --path <项目文件夹路径> --repo <仓库名称>
```

### 创建私有仓库
```bash
python3 upload.py --path <项目文件夹路径> --private
```

## 工作原理

1. 读取目标文件夹中的 `SKILL.md`，提取 frontmatter（name、description）和正文
2. 自动生成 `README.md`（含 Quick Start、完整 SKILL 内容、徽章）
3. 通过 GitHub API 创建或更新仓库
4. Force-push 到 GitHub main 分支

## 输出说明

- 在项目文件夹中生成 `README.md`
- 推送完成后输出 GitHub 仓库地址

## 注意事项

- 目标项目文件夹必须已包含 `SKILL.md`（含 `name:` 和 `description:` 字段）
- 使用 `--force push`，会覆盖远程历史
- 仓库名默认为文件夹名，可通过 `--repo` 覆盖
