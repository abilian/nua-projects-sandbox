import warnings

from sqlalchemy.exc import SAWarning

warnings.simplefilter("ignore", DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)
warnings.simplefilter("ignore", SAWarning)
warnings.simplefilter("ignore", FutureWarning)

from app.main import create_app

assert create_app
