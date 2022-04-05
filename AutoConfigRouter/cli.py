"""This module provides the AutoConfigRouter CLI."""
# AutoConfigRouter/cli.py

from typing import Optional
from pathlib import Path
from openpyxl import load_workbook

import openpyxl
import typer
import AutoConfigRouter.autoconfigrouter


from AutoConfigRouter import __app_name__, __version__, ERRORS, config

app = typer.Typer()

@app.command()
def upload(
    ip_address: str = typer.Option(
        "192.168.1.1",
        "--ip-address",
        "-ip",
        prompt="Set ip address:",
    ),
    login: str = typer.Option(
        "admin",
        "--login",
        "-l",
        prompt="Set login credential:",
    ),
    password: str = typer.Option(
        "password",
        "--passwd",
        "-p",
        prompt="Set password:",
    ),
    file: str = typer.Option(
        r"C:\Users\User\Documents\spreadsheet.xlsx",
        "--file",
        "-f",
        prompt="Set file location:",
    ),
) -> None:
    """Initialize the connection phase."""
    wb = openpyxl.Workbook()
    wb = load_workbook(filename = file, read_only=1)
    ws = wb.active
    w, h = ws.max_row, ws.max_column
    ruleset = [[0 for x in range(w)] for y in range(h)]
    for i in range(2, ws.max_row+1):
        for j in range(1, ws.max_column+1):
            ruleset[i][j] = ws.cell(row=i, column=j)            
    AutoConfigRouter.autoconfigrouter.addRulesCisco(ruleset,login,password,ip_address)

@app.command()
def validate(
    document_path: str = typer.Option(
        r"C:\Users\User\Documents\spreadsheet.xlsx",
        "--document",
        "-d",
        prompt="Select valid document to read ruleset from:",
    ),
) -> None:
    """Acquire rulesets."""
    wb = openpyxl.Workbook()
    wb = load_workbook(filename = document_path, read_only=1)
    ws = wb.active
    for i in range(2, ws.max_row+1):
        for j in range(1, ws.max_column+1):
            cell_obj = ws.cell(row=i, column=j)
            cell_type = ws.cell(row=1, column=j)
            print(cell_type.value,": ", cell_obj.value, end="\n")
        print("\n")

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