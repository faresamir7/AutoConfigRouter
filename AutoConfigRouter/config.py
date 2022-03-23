"""This module provides the AutoConfigRouter config functionality."""
# AutoConfigRouter/config.py

import configparser
from pathlib import Path

import typer

from AutoConfigRouter import (
    CONNECTION_ERROR, CREDENTIAL_ERROR, FILEREAD_ERROR, SUCCESS, __app_name__, SESSION_ERROR, VENDOR_ERROR, OBJECT_ERROR, DIR_ERROR
)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

def init_app() -> int:
    """Initialize the application."""
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    return SUCCESS

def _init_config_file() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILEREAD_ERROR
    return SUCCESS