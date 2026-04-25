import click
import json

from tipster import storage
from tipster.cmd_output import (
    print_success,
    print_error,
)


@click.command()
@click.argument("file_path")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def import_cmd(file_path, yes):
    """Import tips from JSON"""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print_error(f"failed to read file: {e}")
        return

    if isinstance(data, dict):
        tips_data = storage.TipsData.from_dict(data)
    elif isinstance(data, list):
        tips_data = storage.TipsData()
        tips_data.tips = [storage.Tip.from_dict(t) for t in data]
    else:
        print_error("invalid format: expected JSON object or array")
        return

    invalid = []
    for i, tip in enumerate(tips_data.tips):
        if not isinstance(tip.id, str) or not tip.id:
            invalid.append(f"tip {i}: missing or invalid 'id'")
        if not isinstance(tip.topic, str) or not tip.topic:
            invalid.append(f"tip {i}: missing or invalid 'topic'")
        if not isinstance(tip.content, str) or not tip.content:
            invalid.append(f"tip {i}: missing or invalid 'content'")

    if invalid:
        for msg in invalid:
            print_error(msg)
        return

    if not yes and not click.confirm(f"Import {len(tips_data.tips)} tips?"):
        return

    try:
        storage.import_tips(tips_data)
    except Exception as e:
        print_error(f"failed to import: {e}")
        return

    print_success(f"Imported {len(tips_data.tips)} tips")
