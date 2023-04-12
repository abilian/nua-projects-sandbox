from __future__ import annotations

import os

import click
from devtools import debug
from flask import Flask, current_app
from flask.cli import with_appcontext
from rich import print


def register_commands(app: Flask) -> None:
    app.cli.add_command(config)


@click.command(short_help="Show config")
@with_appcontext
def config() -> None:
    config_ = dict(sorted(current_app.config.items()))
    print("CONFIG:")
    debug(config_)
    print()

    print("ENV:")
    env_ = dict(sorted(os.environ.items()))
    debug(env_)
