from datetime import date
from openai import OpenAI

from src.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, WIKI_DIR
from src.ingest import ingest_all

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

MAX_CHARS_PER_FILE = 8000
MAX_TOTAL_CHARS = 120000
BATCH_SIZE = 30000

COMPILATION_PROMPT = """你是一个知识编译器。请将以下原始资料整理成结构化的Markdown知识库。

## 任务要求：

1. **实体识别**：提取所有重要概念、人名、术语，创建独立页面
2. **自动链接**：使用[[双向链接]]语法连接相关概念
3. **层级结构**：
   - 每个实体一个Markdown文件
   - Frontmatter包含：title, date, tags, sources
   - 正文包含：摘要、详细说明、相关链接、待探索问题
4. **冲突处理**：如果多个来源信息矛盾，保留并标注争议点
5. **索引生成**：创建INDEX.md作为知识库入口

## 输出格式要求：

每个页面用 ===FILE: 文件名.md=== 分隔，内容如下：

===FILE: 示例概念.md===
---
title: "示例概念"
date: {today}
tags: ["标签1", "标签2"]
sources: ["来源文件1.pdf", "来源文件2.docx"]
---

# 示例概念

## 摘要
一段简短的概念描述...

## 详细说明
...

## 相关概念
- [[相关概念A]]
- [[相关概念B]]

## 待探索
- [ ] 待深入的问题

## 来源
- `来源文件1.pdf` — 具体引用说明

## 原始资料：
{raw_content}
"""


INCREMENTAL_PROMPT = """你是一个知识编译器。以下是知识库中已有的wiki页面和新增的原始资料。

请根据新增资料：
1. 生成需要新建的wiki页面（格式同上）
2. 列出需要更新的已有页面（给出完整更新后内容）
3. 更新INDEX.md

已有wiki页面：
{existing_wiki}

新增原始资料：
{new_content}

输出格式：每个页面用 ===FILE: 文件名.md=== 分隔。
"""


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n...(内容过长，已截断)..."


def _call_llm(prompt: str) -> str:
    print(f"  发送 {len(prompt)} 字符到 API（模型: {OPENAI_MODEL}）...")
    try:
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=16000,
            temperature=0.3,
        )
        if isinstance(resp, str):
            return resp
        return resp.choices[0].message.content
    except Exception as e:
        print(f"  [API错误] {e}")
        return ""


def _parse_output(text: str) -> dict[str, str]:
    import re
    files = {}
    parts = re.split(r"===FILE:\s*(.+?)===", text)
    i = 1
    while i < len(parts) - 1:
        filename = parts[i].strip()
        content = parts[i + 1].strip()
        if not filename.endswith(".md"):
            filename += ".md"
        files[filename] = content
        i += 2
    return files


def _save_wiki_files(files: dict[str, str]):
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    saved = []
    for filename, content in files.items():
        path = WIKI_DIR / filename
        path.write_text(content, encoding="utf-8")
        saved.append(filename)
    return saved


def compile_all() -> list[str]:
    print("正在解析 raw/ 文件...")
    raw_data = ingest_all()
    if not raw_data:
        print("raw/ 目录中没有可解析的文件")
        return []

    print(f"解析完成，共 {len(raw_data)} 个文件")

    entries = []
    for name, content in raw_data.items():
        truncated = _truncate(content, MAX_CHARS_PER_FILE)
        entries.append((name, truncated))
        print(f"  已加载: {name} ({len(truncated)} 字符)")

    batches = []
    current_batch = []
    current_size = 0
    for name, text in entries:
        entry = f"\n\n--- 文件: {name} ---\n{text}"
        if current_size + len(entry) > BATCH_SIZE and current_batch:
            batches.append(current_batch)
            current_batch = []
            current_size = 0
        current_batch.append((name, entry))
        current_size += len(entry)
    if current_batch:
        batches.append(current_batch)

    print(f"分 {len(batches)} 批编译（每批约 {BATCH_SIZE} 字符）\n")

    all_saved = []
    for i, batch in enumerate(batches, 1):
        raw_text = "".join(entry for _, entry in batch)
        file_names = [name for name, _ in batch]
        print(f"--- 第 {i}/{len(batches)} 批: {', '.join(file_names)} ---")
        print(f"  本批文本: {len(raw_text)} 字符")

        prompt = COMPILATION_PROMPT.format(
            today=date.today().isoformat(),
            raw_content=raw_text,
        )
        result = _call_llm(prompt)
        if not result:
            print(f"  第 {i} 批编译失败，跳过")
            continue
        files = _parse_output(result)
        saved = _save_wiki_files(files)
        all_saved.extend(saved)
        print(f"  生成 {len(saved)} 个页面: {', '.join(saved)}\n")

    print(f"编译完成，共生成 {len(all_saved)} 个wiki页面")
    return all_saved


def compile_incremental(new_files: list[str] | None = None) -> list[str]:
    print("正在解析 raw/ 文件...")
    raw_data = ingest_all()
    if not raw_data:
        return []

    existing_wiki = ""
    for md in sorted(WIKI_DIR.glob("*.md")):
        existing_wiki += f"\n\n--- FILE: {md.name} ---\n{md.read_text(encoding='utf-8')}"

    if new_files:
        new_data = {k: v for k, v in raw_data.items() if k in new_files}
    else:
        wiki_sources = set()
        for md in WIKI_DIR.glob("*.md"):
            content = md.read_text(encoding="utf-8")
            for line in content.splitlines():
                if line.startswith("- `") and "`" in line[3:]:
                    src = line[3:line.index("`", 3)]
                    wiki_sources.add(src)
        new_data = {k: v for k, v in raw_data.items() if k not in wiki_sources}

    if not new_data:
        print("没有发现新增文件")
        return []

    new_text = ""
    for name, content in new_data.items():
        truncated = _truncate(content, MAX_CHARS_PER_FILE)
        new_text += f"\n\n--- 文件: {name} ---\n{truncated}"
        print(f"  新文件: {name} ({len(truncated)} 字符)")

    existing_wiki = _truncate(existing_wiki, MAX_TOTAL_CHARS // 2)

    prompt = INCREMENTAL_PROMPT.format(
        existing_wiki=existing_wiki,
        new_content=new_text,
    )
    print(f"增量编译 {len(new_data)} 个新文件...")
    result = _call_llm(prompt)
    if not result:
        print("增量编译失败：API 未返回内容")
        return []
    files = _parse_output(result)
    saved = _save_wiki_files(files)
    print(f"增量编译完成，更新 {len(saved)} 个wiki页面")
    return saved
