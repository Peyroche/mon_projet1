import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# 📥 Chargement des variables d’environnement depuis .env (utile en local)
load_dotenv()

# ✅ Vérification des variables obligatoires
required_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME"]
for var in required_vars:
    if not os.environ.get(var):
        raise RuntimeError(f"❌ Variable d'environnement manquante : {var}")

# 🔐 Encodage sécurisé du mot de passe MySQL
raw_password = os.environ["DB_PASSWORD"]
encoded_password = quote_plus(raw_password)

# 🧪 Log optionnel pour vérifier le mot de passe encodé
print("Mot de passe brut :", repr(raw_password))
print("Mot de passe encodé :", encoded_password)

class Config:
    # 🔒 Sécurité des cookies
    SESSION_COOKIE_HTTPONLY = True

    # 🔐 Clés secrètes Flask et CSRF
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev_key")
    WTF_CSRF_SECRET_KEY = os.environ.get("CSRF_SECRET_KEY", "csrf_dev_key")

    # 🛠️ Configuration SQLAlchemy avec mot de passe encodé
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ['DB_USER']}:{encoded_password}"
        f"@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 📧 Configuration de l'envoi d’e-mails
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
