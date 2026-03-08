import click
import json
import csv
import io

from tipster import storage
from tipster.cmd_output import (
    print_success,
    print_error,
    console,
)


@click.command()
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Export format",
)
@click.option("--output", "-o", type=click.Path(), help="Output file (default: stdout)")
def export_cmd(format, output):
    """Export tips to JSON or CSV"""
    try:
        data = storage.export()
    except Exception as e:
        print_error(f"failed to export: {e}")
        return

    tips_dict = data.to_dict()
    tips_data = tips_dict.get("tips", [])

    if format == "json":
        content = json.dumps(tips_data, indent=2)
    else:
        if not tips_data:
            content = ""
        else:
            output_buf = io.StringIO()
            fieldnames = [
                "id",
                "topic",
                "content",
                "examples",
                "labels",
                "favorited",
                "created_at",
            ]
            writer = csv.DictWriter(
                output_buf, fieldnames=fieldnames, extrasaction="ignore"
            )
            writer.writeheader()
            for tip in tips_data:
                tip_copy = tip.copy()
                tip_copy["examples"] = "|".join(tip_copy.get("examples", []))
                tip_copy["labels"] = "|".join(tip_copy.get("labels", []))
                writer.writerow(tip_copy)
            content = output_buf.getvalue()

    if output:
        with open(output, "w") as f:
            f.write(content)
        print_success(f"Exported {len(tips_data)} tips to {output}")
    else:
        console.print(content)
