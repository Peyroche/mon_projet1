import os
from urllib.parse import quote_plus

password = quote_plus(os.environ.get("DB_PASSWORD"))

class Config:
    SESSION_COOKIE_HTTPONLY = True
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    WTF_CSRF_SECRET_KEY = os.environ.get("CSRF_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{os.environ.get('DB_USER')}:{password}"
    f"@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")