from __future__ import annotations

import os
import time

import rq_dashboard
from app import views
from devtools import debug
from dynaconf import FlaskDynaconf
from flask import Flask, g, request, session
from flask_talisman import DEFAULT_CSP_POLICY, Talisman
from jinja2 import StrictUndefined

from .cli import register_commands
from .logging import configure_loguru


def create_app(config=None) -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.jinja_env.undefined = StrictUndefined

    configure_app(app, config)

    configure_loguru(app)
    configure_csp(app)

    register_blueprints(app)
    register_commands(app)
    register_perf_watcher(app)
    register_debug_hooks(app)
    register_extra_apps(app)

    return app


def configure_app(app, config) -> None:
    if config:
        # Probably testing
        app.config.from_object(config)
    else:
        FlaskDynaconf(
            app,
            settings_files=["etc/settings.toml", "etc/secrets.toml"],
            load_dotenv=True,
        )

    # FIXME
    app.config = dict(sorted(app.config.items()))

    # Heroku
    database_url = os.environ.get("DATABASE_URL", "")
    if not database_url:
        # Clever Cloud
        database_url = os.environ.get("POSTGRESQL_ADDON_URI", "")

    if database_url.startswith("postgres:"):
        database_url = database_url.replace("postgres:", "postgresql:")

    if database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    redis_url = os.environ.get("REDISCLOUD_URL", "")
    if redis_url:
        app.config["REDIS_URL"] = redis_url


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(views.blueprint)


def register_debug_hooks(app: Flask) -> None:
    if not app.config.get("DEBUG_CONFIG"):
        return

    @app.before_request
    def before_request() -> None:
        debug("before_request")

    @app.before_request
    def dump_cookies() -> None:
        debug(
            dict(**session),
            g.user,
        )

    config_ = dict(sorted(app.config.items()))
    print("CONFIG:")
    debug(config_)
    print()

    print("ENV:")
    env_ = dict(sorted(os.environ.items()))
    debug(env_)


def configure_csp(app: Flask) -> None:
    if not app.debug:
        csp = app.config.get("CONTENT_SECURITY_POLICY", DEFAULT_CSP_POLICY)
        Talisman(app, content_security_policy=csp)


def register_perf_watcher(app: Flask) -> None:
    class Timer:
        def __init__(self) -> None:
            self.start = time.time()
            self.url = request.url

        def elapsed(self) -> float:
            return time.time() - self.start

        def info(self) -> str:
            return f"Request {self.url} took {self.elapsed():.2f}s"

    @app.before_request
    def start_timer() -> None:
        g.timer = Timer()


def register_extra_apps(app: Flask) -> None:
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")
