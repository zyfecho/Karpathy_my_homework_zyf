---
title: "开发工具与AI辅助"
date: 2026-04-28
tags: ["开发工具", "AI", "Claude Code", "Copilot"]
sources: ["claude code(cc).pdf", "CC switch配置CC教程（使用LX API中转站）.pdf", "VScode部署copilot以及pro版本申请.docx"]
---

# 开发工具与 AI 辅助

现代嵌入式开发中可借助 AI 编程工具提升效率，包括 Claude Code、GitHub Copilot 等。

## Claude Code (CC)

Claude Code 是一个基于终端命令行的 AI 编程助手，可以：

- 根据自然语言指令生成代码、智能调试、优化性能
- 通过终端命令行交互，集成到日常开发流程
- 集成到 VSCode 等编辑器中以面板形式使用

### 配置要点

- **CLAUDE.md 规则文件**：写入项目背景、代码风格、技术栈等规则，CC 每次启动都会读取，生成的代码更符合要求
- **CC Switch**：可将 CC 默认的 Claude 模型切换为国内大模型（火山方舟、智谱等），网络不好时也能流畅使用

### CC Switch 配置（使用 LX API 中转站）

1. 打开控制台 → 令牌管理
2. 找到令牌，点击聊天按钮右侧展开菜单 → 一键导入 CC Switch
3. 分组选 FreeClaude（稳定分组）
4. 按提示完成导入

> 注意：不要在截图、日志或公开内容中泄露以 `sk-` 开头的 API Key。

### 模型选择

Claude Code 可接入多种 AI 模型的 API，其中智谱清言 GLM 有免费额度，其他不同程度收费。

## GitHub Copilot（VSCode）

1. 在 VSCode 扩展中搜索 GitHub Copilot，点击安装
2. 右下角提示登录 GitHub 网址，绑定账号
3. 点击 authorize 授权即可

学生可申请 Pro 版本免费使用。

## 相关主题

- [[dev-environment]] — Keil 与 CubeMX 开发环境
- [[career-advice]] — AI 工具在求职中的价值

## 来源

- `claude code(cc).pdf` — Claude Code 安装教程、CC Switch 配置、核心功能介绍
- `CC switch配置CC教程（使用LX API中转站）.pdf` — CC Switch 一键导入步骤与注意事项
- `VScode部署copilot以及pro版本申请.docx` — VSCode Copilot 安装与学生认证
