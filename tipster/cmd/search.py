import click

from tipster import storage
from tipster.cmd_output import (
    print_tips_list,
    print_error,
)


@click.command()
@click.argument("query")
def search(query):
    """Search tips by content or labels"""
    try:
        tips = storage.search_tips(query)
    except Exception as e:
        print_error(f"search failed: {e}")
        return

    print_tips_list(tips, f"Search Results ({len(tips)})")
