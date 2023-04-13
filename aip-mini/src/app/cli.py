from __future__ import annotations

import os
import sys

import click
from flask import Flask, current_app
from flask.cli import with_appcontext
from rich import print
from snoop import pp


def register_commands(app: Flask) -> None:
    app.cli.add_command(config)


@click.command(short_help="Show config")
@with_appcontext
def config() -> None:
    config_ = dict(sorted(current_app.config.items()))
    print("CONFIG:", file=sys.stderr)
    pp(config_)
    print()

    print("ENV:", file=sys.stderr)
    env_ = dict(sorted(os.environ.items()))
    pp(env_)
