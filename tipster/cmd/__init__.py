import click
from importlib.metadata import version as pkg_version

from tipster.cmd_output import (  # noqa: F401
    print_tip,
    print_tips_list,
    print_topics,
    print_config,
    print_success,
    print_error,
    console,
)


def _get_version() -> str:
    try:
        return pkg_version("tipster")
    except Exception:
        return "0.2.0"


@click.group()
@click.version_option(version=_get_version())
def cli():
    """AI-powered CLI tip generator"""
    pass


# Import submodules to register their commands
from tipster.cmd import (  # noqa: E402
    tips,
    fav,
    topics,
    config_cmd,
    export,
    import_cmd,
    search,
    version,
)

# Add subcommands to cli
cli.add_command(tips.tips)
cli.add_command(fav.fav)
cli.add_command(topics.topics)
cli.add_command(config_cmd.config_cmd)
cli.add_command(export.export_cmd)
cli.add_command(import_cmd.import_cmd)
cli.add_command(search.search)
cli.add_command(version.version)
