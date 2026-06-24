import click
from rich import box
from rich.panel import Panel

from tipster import config, storage
from tipster.cmd import _get_version
from tipster.cmd_output import console


@click.command()
def version():
    """Show version"""
    console.print(
        Panel(
            f"[bold #e94560]tipster[/] {_get_version()}\n\n"
            f"[dim]Config:[/dim] {config.get_config_path()}\n"
            f"[dim]Tips:[/dim] {storage.get_tips_path()}",
            title="Version Info",
            border_style="#e94560",
            box=box.ROUNDED,
        )
    )
