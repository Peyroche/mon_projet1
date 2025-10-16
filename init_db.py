from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/home/MD/mon_projet1/.env")  # ← chemin absolu

print("DB_HOST =", os.getenv("DB_HOST"))  # ← test d'affichage

from app import app, db

with app.app_context():
    db.create_all()
    print("✅ Tables créées avec succès.")



