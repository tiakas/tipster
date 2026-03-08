import click

from tipster import config, storage, ai
from tipster.cmd_output import (
    print_tip,
    print_topics,
    print_success,
    print_error,
    console,
)


@click.group()
def topics():
    """Manage topics"""
    pass


@topics.command(name="new")
@click.argument("topic")
def topics_new(topic):
    """Add a topic and generate a tip for it"""
    cfg = config.load()

    if not cfg.provider:
        print_error("please configure tipster first: tipster config")
        return

    api_key = config.get_api_key(cfg.provider)
    client = ai.get_client(cfg.provider, api_key, cfg.model)

    if not client:
        print_error(f"unknown provider: {cfg.provider}")
        return

    console.print(f"[bold]Generating tip for '{topic}'...[/bold]")

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

    if topic not in cfg.topics:
        cfg.topics.append(topic)
        config.save(cfg)

    print_success(f"Tip added for '{topic}'")
    print_tip(tip)


@topics.command(name="list")
def topics_list():
    """List all topics"""
    cfg = config.load()
    tips_topics = storage.get_all_topics()

    all_topics = sorted(set(cfg.topics + tips_topics))

    topics_data = [
        (topic, len(storage.get_tips_by_topic(topic))) for topic in all_topics
    ]
    print_topics(topics_data)


@topics.command(name="delete")
@click.argument("topic")
def topics_delete(topic):
    """Remove a topic and all its tips"""
    try:
        storage.remove_topic(topic)
    except Exception as e:
        print_error(f"failed to remove topic: {e}")
        return

    cfg = config.load()
    if topic in cfg.topics:
        cfg.topics.remove(topic)
        config.save(cfg)

    print_success(f"Removed topic '{topic}' and all its tips")
