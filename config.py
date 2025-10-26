import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

required_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME"]
for var in required_vars:
    if not os.environ.get(var):
        raise RuntimeError(f"❌ Variable d'environnement manquante : {var}")

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev_key")
    WTF_CSRF_SECRET_KEY = os.environ.get("CSRF_SECRET_KEY", "csrf_dev_key")
    SESSION_COOKIE_HTTPONLY = True

    if os.environ.get("FLASK_ENV") == "production":
        encoded_password = quote_plus(os.environ.get("DB_PASSWORD", ""))
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{os.environ['DB_USER']}:{encoded_password}"
            f"@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost:3306/ma_base_locale"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "connect_args": {"connect_timeout": 10}
    }
