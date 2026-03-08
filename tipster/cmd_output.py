from rich.console import Console
from rich.panel import Panel
from rich import box as rich_box

console = Console()


def print_header(text: str) -> None:
    console.print(f"\n[bold #e94560]{text}[/]")


def print_success(text: str) -> None:
    console.print(f"[bold #2ecc71]✓[/] {text}")


def print_error(text: str) -> None:
    console.print(f"[bold red]✗[/] {text}", style="red")


def print_tip(tip, show_id: bool = True) -> None:
    content = f"[bold #e94560]Topic:[/] {tip.topic}\n\n{tip.content}"

    if tip.examples:
        content += "\n\n[bold #3498db]Examples:[/]"
        for ex in tip.examples:
            content += f"\n  📝 {ex}"

    if tip.labels:
        labels_str = ", ".join(f"[link=#{label}]{label}[/link]" for label in tip.labels)
        content += f"\n\n[bold #9b59b6]Labels:[/] {labels_str}"

    if show_id:
        content += f"\n\n[dim]ID: {tip.id[:8]}[/dim]"

    console.print(
        Panel(
            content,
            border_style="#3d3d5c",
            box=rich_box.ROUNDED,
            padding=(1, 2),
        )
    )


def print_tips_list(tips, title: str = "Tips") -> None:
    from rich.table import Table

    if not tips:
        console.print("[dim]No tips found[/dim]")
        return

    table = Table(title=title, box=rich_box.SIMPLE, show_lines=True)
    table.add_column("ID", style="dim", width=10, no_wrap=True)
    table.add_column("", width=2)
    table.add_column("Topic", style="#e94560", no_wrap=True)
    table.add_column("Content", style="#eaeaea", no_wrap=False)

    for tip in tips:
        star = "⭐" if tip.favorited else ""
        content = tip.content[:60] + "..." if len(tip.content) > 60 else tip.content
        table.add_row(tip.id[:8], star, tip.topic, content)

    console.print(table)


def print_topics(topics) -> None:
    from rich.table import Table

    if not topics:
        console.print("[dim]No topics configured[/dim]")
        return

    table = Table(title="Topics", box=rich_box.ROUNDED, show_header=False)
    table.add_column("Topic", style="#e94560", no_wrap=True)
    table.add_column("Tips", style="#7f8c8d", justify="right", width=8)

    for topic, count in topics:
        table.add_row(f"📁 {topic}", f"[{count}]")

    console.print(table)


def print_config(cfg) -> None:
    from rich.table import Table

    data = [
        ("Provider", cfg.provider or "[dim]not set[/dim]"),
        ("Model", cfg.model or "[dim]default[/dim]"),
        ("API Key", "[dim]set[/dim]" if cfg.api_key else "[dim]env var[/dim]"),
        ("Topics", str(len(cfg.topics))),
    ]

    table = Table(box=rich_box.SIMPLE, show_header=False)
    table.add_column("Key", style="#e94560")
    table.add_column("Value", style="#eaeaea")

    for key, value in data:
        table.add_row(key, value)

    console.print(
        Panel(
            table, title="⚙️ Configuration", border_style="#e94560", box=rich_box.ROUNDED
        )
    )
