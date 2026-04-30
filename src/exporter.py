import markdown
from pathlib import Path

from src.config import WIKI_DIR, BASE_DIR

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 16px; border-radius: 6px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f8f8f8; }}
        a {{ color: #0066cc; }}
    </style>
</head>
<body>
{content}
</body>
</html>"""


def export_to_html(output_dir: Path | None = None) -> list[Path]:
    if output_dir is None:
        output_dir = BASE_DIR / "outputs" / "html"
    output_dir.mkdir(parents=True, exist_ok=True)

    md_ext = ["tables", "fenced_code", "toc"]
    exported = []

    for md_file in sorted(WIKI_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        if text.startswith("---"):
            end = text.find("---", 3)
            if end != -1:
                text = text[end + 3:].strip()

        html_body = markdown.markdown(text, extensions=md_ext)
        html_body = html_body.replace("[[", '<a href="').replace("]]", '.html">[link]</a>')

        title = md_file.stem.replace("-", " ").title()
        full_html = HTML_TEMPLATE.format(title=title, content=html_body)

        out_path = output_dir / f"{md_file.stem}.html"
        out_path.write_text(full_html, encoding="utf-8")
        exported.append(out_path)

    return exported


def export_to_single_html(output_path: Path | None = None) -> Path:
    if output_path is None:
        output_path = BASE_DIR / "outputs" / "knowledge-base-full.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    md_ext = ["tables", "fenced_code"]
    all_html = []

    for md_file in sorted(WIKI_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        if text.startswith("---"):
            end = text.find("---", 3)
            if end != -1:
                text = text[end + 3:].strip()
        html_body = markdown.markdown(text, extensions=md_ext)
        all_html.append(f'<section id="{md_file.stem}">\n{html_body}\n</section>\n<hr>')

    full = HTML_TEMPLATE.format(
        title="嵌入式软件开发知识库",
        content="\n".join(all_html),
    )
    output_path.write_text(full, encoding="utf-8")
    return output_path
