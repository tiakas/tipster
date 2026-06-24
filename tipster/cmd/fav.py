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
    tips_data = storage.load()
    matches = [tip for tip in tips_data.tips if tip.id.startswith(tip_id)]

    if not matches:
        print_error(f"tip not found: {tip_id}")
        return
    if len(matches) > 1:
        print_error(
            f"ambiguous ID prefix '{tip_id}' matches {len(matches)} tips. Use a longer prefix"
        )
        return

    tip = matches[0]
    if tip.favorited:
        print_success("Already in favorites")
        return

    tip.favorited = True
    storage.save(tips_data)
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
    matches = [tip for tip in tips_data.tips if tip.id.startswith(tip_id)]

    if not matches:
        print_error(f"tip not found: {tip_id}")
        return
    if len(matches) > 1:
        print_error(
            f"ambiguous ID prefix '{tip_id}' matches {len(matches)} tips. Use a longer prefix"
        )
        return

    tip = matches[0]
    if not tip.favorited:
        print_error(f"tip not favorited: {tip_id}")
        return

    tip.favorited = False
    storage.save(tips_data)
    print_success("Removed from favorites")
