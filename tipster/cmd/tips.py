import click
import random
import requests

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
        response = ai.generate_with_retry(client, topic)
    except ValueError as e:
        print_error(f"invalid topic: {e}")
        return
    except requests.exceptions.Timeout:
        print_error("request timed out")
        return
    except requests.exceptions.ConnectionError:
        print_error("network error - check your connection")
        return
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
    matches = storage.find_tips_by_prefix(tip_id)
    if not matches:
        print_error(f"tip not found: {tip_id}")
        return
    if len(matches) > 1:
        print_error(
            f"ambiguous ID prefix '{tip_id}' matches {len(matches)} tips. Use a longer prefix"
        )
        return
    print_tip(matches[0])


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
@click.option("--label", "-l", help="Filter by label (case-insensitive)")
@click.option("--limit", "-n", type=int, help="Show at most N tips")
def tips_list(topic, label, limit):
    """Show all tips or tips for a specific topic"""
    if topic:
        tips = storage.get_tips_by_topic(topic)
    else:
        data = storage.load()
        tips = data.tips

    if label:
        label_lower = label.lower()
        tips = [t for t in tips if any(label_lower in lb.lower() for lb in t.labels)]

    total = len(tips)
    if limit is not None and limit >= 0:
        tips = tips[:limit]

    if limit is not None and len(tips) < total:
        title = f"Tips ({len(tips)} of {total})"
    else:
        title = f"Tips ({total})"
    print_tips_list(tips, title)


@tips.command(name="random")
@click.argument("topic", required=False)
def tips_random(topic):
    """Show a random saved tip"""
    if topic:
        tips = storage.get_tips_by_topic(topic)
    else:
        tips = storage.load().tips

    if not tips:
        print_error("no tips found")
        return

    print_tip(random.choice(tips))
