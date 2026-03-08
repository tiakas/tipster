import click

from tipster import storage
from tipster.cmd_output import (
    print_tips_list,
    print_success,
    print_error,
)


@click.group()
def fav():
    """Manage favorites"""
    pass


@fav.command(name="add")
@click.argument("tip_id")
def fav_add(tip_id):
    """Add a tip to favorites"""
    tip = storage.toggle_favorite(tip_id)
    if not tip:
        print_error(f"tip not found: {tip_id}")
        return
    print_success("Added to favorites")


@fav.command(name="list")
def fav_list():
    """Show all favorite tips"""
    try:
        tips = storage.get_favorites()
    except Exception as e:
        print_error(str(e))
        return

    print_tips_list(tips, f"Favorites ({len(tips)})")


@fav.command(name="remove")
@click.argument("tip_id")
def fav_remove(tip_id):
    """Remove a tip from favorites"""
    tips_data = storage.load()

    found = False
    for tip in tips_data.tips:
        if tip.id.startswith(tip_id):
            if tip.favorited:
                tip.favorited = False
                found = True
            break

    if found:
        storage.save(tips_data)
        print_success("Removed from favorites")
    else:
        print_error(f"tip not found or not favorited: {tip_id}")
