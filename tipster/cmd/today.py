import click
import random
from datetime import datetime, timezone

from tipster import config, storage, ai
from tipster.cmd_output import (
    print_tip,
    print_error,
    console,
)


@click.command()
@click.argument("topic", required=False)
@click.option("--new", "-n", is_flag=True, help="Force a fresh tip, ignoring cache")
def today(topic, new):
    """Show today's tip (generated once per day, cached)"""
    cfg = config.load()
    today_str = datetime.now(timezone.utc).date().isoformat()

    if not new and cfg.today_date == today_str and cfg.today_tip_id:
        tip = storage.get_tip_by_id(cfg.today_tip_id)
        if tip:
            print_tip(tip)
            return

    if not cfg.provider:
        print_error("please configure tipster first: tipster config")
        return

    if not topic:
        topics = storage.get_all_topics() or cfg.topics
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

    console.print(f"[bold]Generating today's tip about {topic}...[/bold]")

    try:
        response = ai.generate_with_retry(client, topic)
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

    cfg.today_date = today_str
    cfg.today_tip_id = tip.id
    try:
        config.save(cfg)
    except Exception as e:
        print_error(f"failed to save config: {e}")

    print_tip(tip)
