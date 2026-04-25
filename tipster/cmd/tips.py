import click
import random

from tipster import config, storage, ai
from tipster.cmd_output import (
    print_tip,
    print_tips_list,
    print_success,
    print_error,
    console,
)


@click.group()
def tips():
    """Manage tips"""
    pass


@tips.command(name="new")
@click.argument("topic", required=False)
def tips_new(topic):
    """Display a new tip (generate about a topic)"""
    cfg = config.load()

    if not cfg.provider:
        print_error("please configure tipster first: tipster config")
        return

    if not topic:
        topics = storage.get_all_topics()
        if not topics:
            print_error(
                "no topics configured. Add a topic with 'tipster topics new <topic>'"
            )
            return
        topic = random.choice(topics)

    api_key = config.get_api_key(cfg.provider)
    client = ai.get_client(cfg.provider, api_key, cfg.model)

    if not client:
        print_error(f"unknown provider: {cfg.provider}")
        return

    console.print(f"[bold]Generating new tip about {topic}...[/bold]")

    try:
        response = client.generate_tip(topic)
    except Exception as e:
        print_error(f"failed to generate tip: {e}")
        return

    try:
        tip = storage.add_tip(
            topic, response.content, response.examples, response.labels
        )
    except Exception as e:
        print_error(f"failed to save tip: {e}")
        return

    print_tip(tip)


@tips.command(name="show")
@click.argument("tip_id")
def tips_show(tip_id):
    """Show a tip by ID"""
    tip = storage.get_tip_by_id(tip_id)
    if not tip:
        print_error(f"tip not found: {tip_id}")
        return
    print_tip(tip)


@tips.command(name="delete")
@click.argument("tip_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def tips_delete(tip_id, yes):
    """Delete a tip by ID"""
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

    display_id = tip_id[:8] if len(tip_id) > 8 else tip_id

    if not yes and not click.confirm(f"Delete tip {display_id}?"):
        return

    tips_data.tips = [tip for tip in tips_data.tips if not tip.id.startswith(tip_id)]
    try:
        storage.save(tips_data)
    except Exception as e:
        print_error(f"failed to save: {e}")
        return

    print_success(f"Deleted tip {display_id}")


@tips.command(name="list")
@click.argument("topic", required=False)
def tips_list(topic):
    """Show all tips or tips for a specific topic"""
    if topic:
        tips = storage.get_tips_by_topic(topic)
    else:
        data = storage.load()
        tips = data.tips

    print_tips_list(tips, f"Tips ({len(tips)})")
