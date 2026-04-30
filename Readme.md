# my-knowledge-base
# Karpathy 风格长上下文知识库

基于 STM32 / FreeRTOS / 嵌入式软件开发资料的个人知识库构建与问答实践。

## 项目简介

本项目实现了一个符合 Karpathy 理念的知识库系统。无需向量数据库，不依赖传统 RAG 检索，而是将原始资料（`raw/`）通过 LLM 编译为结构化的 Markdown Wiki（`wiki/`），问答阶段让模型直接阅读整个知识库，实现全量上下文召回与跨文档综合推理。

## 核心特性

- **Ingest**：支持 PDF、DOCX、PPTX、HTML、Markdown 等多格式资料导入
- **Compile**：基于 **GPT-5.4**（1M 上下文）自动提取实体、概念、摘要，生成带 Frontmatter 和双向链接的 Wiki 页面
- **Query**：整库问答，支持多轮对话与来源溯源
- **Lint**：自动检测死链、孤立页面、Frontmatter 问题
- **Obsidian 兼容**：`wiki/` 可直接用 Obsidian 打开，享受图谱视图与反向链接

## 技术栈

- Python 3.10+
- **OpenAI GPT-5.4**（2026年3月发布，上下文 1M tokens）
- Obsidian（可选，用于可视化）

## 数据统计

截至提交前：
- `raw/` 原始资料：24 份
- `wiki/` 知识页面：17 篇
- 双向链接总数：89 条
