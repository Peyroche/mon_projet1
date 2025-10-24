import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# 📥 Chargement des variables d’environnement depuis .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev_key")
    WTF_CSRF_SECRET_KEY = os.environ.get("CSRF_SECRET_KEY", "csrf_dev_key")
    SESSION_COOKIE_HTTPONLY = True

    if os.environ.get("FLASK_ENV") == "production":
        raw_password = os.environ.get("DB_PASSWORD", "")
        encoded_password = quote_plus(raw_password)
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

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_TIMEOUT = 10  # en secondes