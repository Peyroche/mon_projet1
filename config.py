import os
from urllib.parse import quote_plus

# 🔐 Encodage sécurisé du mot de passe AVANT la classe
raw_password = os.environ.get("DB_PASSWORD", "")
encoded_password = quote_plus(raw_password)

# 🧪 Vérification dans les logs
print("Mot de passe brut :", raw_password)
print("Mot de passe encodé :", encoded_password)

# ⚠️ Déclenche une erreur si le mot de passe est absent
if not raw_password:
    raise ValueError("⚠️ DB_PASSWORD est manquant ou vide")

class Config:
    # 🔒 Sécurité des cookies
    SESSION_COOKIE_HTTPONLY = True

    # 🔐 Clés secrètes Flask et CSRF
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    WTF_CSRF_SECRET_KEY = os.environ.get("CSRF_SECRET_KEY")

    # 🛠️ Configuration SQLAlchemy avec mot de passe encodé
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ.get('DB_USER')}:{encoded_password}"
        f"@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 📧 Configuration de l'envoi d'e-mails
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
