import click

from tipster import config, ai
from tipster.cmd_output import (
    print_config,
    print_success,
    print_error,
)


@click.command()
@click.option(
    "--provider",
    "-p",
    help="Set AI provider (openai, anthropic, gemini, deepseek, glm, ollama)",
)
@click.option("--model", "-m", help="Set AI model")
@click.option("--apikey", "-k", is_flag=True, help="Set API key (interactive prompt)")
@click.option("--show", "-s", is_flag=True, help="Show current configuration")
def config_cmd(provider, model, apikey, show):
    """Configuration settings"""
    cfg = config.load()

    if show:
        print_config(cfg)
        return

    changed = False

    if provider:
        if not ai.has_provider(provider):
            print_error(
                f"unknown provider: {provider}. Available: {', '.join(ai.get_provider_names())}"
            )
            return
        cfg.provider = provider
        changed = True

    if model:
        cfg.model = model
        changed = True

    if apikey:
        key = click.prompt("API key", hide_input=True)
        cfg.api_key = key
        changed = True

    if changed:
        config.save(cfg)
        print_success("Configuration saved")
    else:
        print_config(cfg)
