import click
from rich import box
from rich.panel import Panel

from importlib.metadata import version as pkg_version

from tipster import config, storage
from tipster.cmd_output import console


def _get_version() -> str:
    try:
        return pkg_version("tipster")
    except Exception:
        return "0.2.0"


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
