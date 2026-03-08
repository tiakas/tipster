import click
import json

from tipster import storage
from tipster.cmd_output import (
    print_success,
    print_error,
)


@click.command()
@click.argument("file_path")
def import_cmd(file_path):
    """Import tips from JSON"""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print_error(f"failed to read file: {e}")
        return

    if isinstance(data, dict):
        tips_data = storage.TipsData.from_dict(data)
    else:
        tips_data = storage.TipsData()
        tips_data.tips = [storage.Tip.from_dict(t) for t in data]

    try:
        storage.import_tips(tips_data)
    except Exception as e:
        print_error(f"failed to import: {e}")
        return

    print_success(f"Imported {len(tips_data.tips)} tips")
