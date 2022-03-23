"""This module provides the AutoConfigRouter CLI."""
# AutoConfigRouter/cli.py

from typing import Optional
from pathlib import Path

import typer

from AutoConfigRouter import __app_name__, __version__, ERRORS, config

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        "192.168.1.1",
        "--ip-address",
        "-ip",
        prompt="Set ip address:",
    ),
) -> None:
    """Initialize the connection phase."""
    app_init_error = config.init_app()
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return