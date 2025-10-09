from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os

user = "433809"
password = quote_plus("+2422301Mn")
host = "mysql-mdconsulting.alwaysdata.net"
db = "mdconsulting_admin"

uri = f"mysql+pymysql://{user}:{password}@{host}/{db}"
engine = create_engine(uri)

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ Connexion réussie :", result.scalar())
except Exception as e:
    print("❌ Échec de connexion :", e)
