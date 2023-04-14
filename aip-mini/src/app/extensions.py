from __future__ import annotations

# from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_babel import Babel
from flask_mailing import Mail
from flask_migrate import Migrate
from flask_rq2 import RQ
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_vite import Vite
from pytz import timezone
from sqlalchemy.orm import declarative_base

# from app.flask.lib.wakaq import WakaQ
# from app.models.base import Base
#
# oauth = OAuth()

Base = declarative_base()

db = SQLAlchemy(model_class=Base)
# db = Alchemical(model_class=Base)

mail = Mail()

migrate = Migrate()
rq = RQ()

PARIS_TZ = timezone("Europe/Paris")
babel = Babel(default_locale="fr", default_timezone=PARIS_TZ)
# TODO: use localeselector() like in abilian-core

security = Security()
vite = Vite()


# wakaq = WakaQ()

# session = Session()

# # Define models
# fsqla.FsModels.set_db_info(db)


# @email_dispatched.connect_via(ANY)
# def debug_email(msg, app) -> None:
#     if not app.debug:
#         return
#     debug(vars(msg))


def register_extensions(app: Flask) -> None:
    # oauth.init_app(app)

    db.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db)
    vite.init_app(app)
    rq.init_app(app)
    # wakaq.init_app(app)

    # setup_security(app, db)


# def setup_security(app: Flask, db: SQLAlchemy) -> None:
#     """Setup Flask-Security"""
#     from app.models.auth import Role, User
#
#     user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
#     security.init_app(app, user_datastore)
