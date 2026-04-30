import re
from src.config import WIKI_DIR


def _load_all_pages() -> dict[str, str]:
    pages = {}
    for md in sorted(WIKI_DIR.glob("*.md")):
        pages[md.stem] = md.read_text(encoding="utf-8")
    return pages


def _extract_links(content: str) -> set[str]:
    return set(re.findall(r"\[\[(.+?)\]\]", content))


def find_dead_links() -> list[dict]:
    pages = _load_all_pages()
    page_names = set(pages.keys())
    issues = []
    for name, content in pages.items():
        links = _extract_links(content)
        for link in links:
            if link not in page_names:
                issues.append({"type": "dead_link", "file": f"{name}.md", "link": link})
    return issues


def find_orphan_pages() -> list[dict]:
    pages = _load_all_pages()
    all_linked = set()
    for content in pages.values():
        all_linked.update(_extract_links(content))
    exempt = {"INDEX", "README"}
    orphans = []
    for name in pages:
        if name in exempt:
            continue
        if name not in all_linked:
            orphans.append({"type": "orphan", "file": f"{name}.md"})
    return orphans


def find_empty_pages(min_chars: int = 100) -> list[dict]:
    pages = _load_all_pages()
    issues = []
    for name, content in pages.items():
        if len(content.strip()) < min_chars:
            issues.append({"type": "empty", "file": f"{name}.md", "chars": len(content.strip())})
    return issues


def check_frontmatter() -> list[dict]:
    required_fields = {"title", "date", "tags", "sources"}
    pages = _load_all_pages()
    issues = []
    for name, content in pages.items():
        if name == "INDEX":
            continue
        if not content.startswith("---"):
            issues.append({"type": "no_frontmatter", "file": f"{name}.md"})
            continue
        end = content.find("---", 3)
        if end == -1:
            issues.append({"type": "bad_frontmatter", "file": f"{name}.md"})
            continue
        fm_text = content[3:end]
        found = set()
        for line in fm_text.splitlines():
            if ":" in line:
                key = line.split(":")[0].strip()
                found.add(key)
        missing = required_fields - found
        if missing:
            issues.append({"type": "missing_fields", "file": f"{name}.md", "missing": list(missing)})
    return issues


def lint_all() -> list[dict]:
    issues = []
    issues.extend(find_dead_links())
    issues.extend(find_orphan_pages())
    issues.extend(find_empty_pages())
    issues.extend(check_frontmatter())
    return issues
