import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rich.console import Console
from rich.table import Table

console = Console()


def cmd_ingest(args):
    from src.ingest import list_raw_files
    files = list_raw_files()
    table = Table(title="raw/ 文件列表")
    table.add_column("文件名", style="cyan")
    table.add_column("格式", style="green")
    table.add_column("大小(KB)", justify="right")
    table.add_column("可解析", justify="center")
    for f in files:
        status = "[green]YES[/green]" if f["supported"] else "[red]NO[/red]"
        table.add_row(f["name"], f["ext"], str(f["size_kb"]), status)
    console.print(table)
    supported = sum(1 for f in files if f["supported"])
    console.print(f"\n共 {len(files)} 个文件，{supported} 个可解析")


def cmd_compile(args):
    if args.incremental:
        from src.compiler import compile_incremental
        saved = compile_incremental()
    else:
        from src.compiler import compile_all
        saved = compile_all()
    if saved:
        console.print(f"[green]生成/更新了 {len(saved)} 个页面:[/green]")
        for name in saved:
            console.print(f"  wiki/{name}")


def cmd_query(args):
    from src.query_engine import KarpathyKnowledgeBase
    kb = KarpathyKnowledgeBase()
    console.print("[dim]加载知识库完成[/dim]\n")
    answer = kb.query(args.question)
    console.print(answer)
    path = kb.save_session()
    if path:
        console.print(f"\n[dim]会话已保存: {path}[/dim]")


def cmd_chat(args):
    from src.query_engine import KarpathyKnowledgeBase
    kb = KarpathyKnowledgeBase()
    console.print("[green]知识库已加载，输入问题开始对话（输入 quit 退出）[/green]\n")
    while True:
        try:
            question = console.input("[bold cyan]Q: [/bold cyan]")
        except (EOFError, KeyboardInterrupt):
            break
        if question.strip().lower() in ("quit", "exit", "q"):
            break
        if not question.strip():
            continue
        answer = kb.query(question)
        console.print(f"\n[bold green]A:[/bold green] {answer}\n")
    path = kb.save_session()
    if path:
        console.print(f"\n[dim]会话已保存: {path}[/dim]")


def cmd_lint(args):
    from src.linter import lint_all
    issues = lint_all()
    if not issues:
        console.print("[green]知识库健康检查通过，未发现问题[/green]")
        return
    table = Table(title="知识库健康检查报告")
    table.add_column("类型", style="red")
    table.add_column("文件", style="cyan")
    table.add_column("详情")
    for issue in issues:
        detail = ""
        if "link" in issue:
            detail = f"[[{issue['link']}]]"
        elif "missing" in issue:
            detail = ", ".join(issue["missing"])
        elif "chars" in issue:
            detail = f"{issue['chars']} 字符"
        table.add_row(issue["type"], issue["file"], detail)
    console.print(table)
    console.print(f"\n共发现 {len(issues)} 个问题")


def cmd_export(args):
    from src.exporter import export_to_html, export_to_single_html
    if args.format == "html":
        exported = export_to_html()
        console.print(f"[green]导出 {len(exported)} 个HTML文件到 outputs/html/[/green]")
    elif args.format == "single":
        path = export_to_single_html()
        console.print(f"[green]导出完成: {path}[/green]")


def main():
    parser = argparse.ArgumentParser(description="Karpathy风格知识库管理工具")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("ingest", help="查看raw/中的文件列表和解析状态")

    p_compile = sub.add_parser("compile", help="编译知识库")
    p_compile.add_argument("--incremental", action="store_true", help="增量编译")

    p_query = sub.add_parser("query", help="单次问答")
    p_query.add_argument("question", help="问题内容")

    sub.add_parser("chat", help="交互式多轮对话")

    sub.add_parser("lint", help="知识库健康检查")

    p_export = sub.add_parser("export", help="导出知识库")
    p_export.add_argument("--format", choices=["html", "single"], default="html", help="导出格式")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return

    commands = {
        "ingest": cmd_ingest,
        "compile": cmd_compile,
        "query": cmd_query,
        "chat": cmd_chat,
        "lint": cmd_lint,
        "export": cmd_export,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
