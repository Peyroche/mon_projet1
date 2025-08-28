from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import session
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_mail import Message
import requests
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from dotenv import load_dotenv
from validator import validate_signup_data, validate_commande_data, validate_contact_data
import os

load_dotenv()  # Charge les variables depuis .env
print(os.environ.get("FLASK_SECRET_KEY"))
if not os.environ.get("FLASK_SECRET_KEY"):
    raise RuntimeError("FLASK_SECRET_KEY est introuvable. Vérifie ton fichier .env.")

# Clés secrètes
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config["WTF_CSRF_SECRET_KEY"] = os.environ.get("CSRF_SECRET_KEY")

print("FLASK_SECRET_KEY:", app.secret_key)
print("CSRF_SECRET_KEY:", app.config["WTF_CSRF_SECRET_KEY"])

# Sécurité des cookies de session
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Pour éviter les vols de session

csrf = CSRFProtect(app)

# 🔧 Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}"
    f"@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
)
db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")
)
mail = Mail(app)

# 🛍️ Modèle commande
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.Column(db.String(500), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255))  # nom du fichier image

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    motdepasse = db.Column(db.String(255), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)

class MessageContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

with app.app_context():
    db.create_all()

# 📦 Route API commandes
@app.route("/valider_commande", methods=["POST"])
def valider_commande():
    if not request.is_json:
        return jsonify({"success": False, "error": "Requête non JSON"}), 400

    data = request.get_json()

    # 🔍 Validation des données
    errors = validate_commande_data(data)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    # ✅ Extraction des données après validation
    nom = data.get("nom")
    prenom = data.get("prenom")
    adresse = data.get("adresse")
    telephone = data.get("telephone")
    email = data.get("email")
    panier = data.get("panier", [])
    total = float(data.get("total", 0))

    items = ", ".join([f"{item['produit']} ({item['prix']}€)" for item in panier])

    nouvelle_commande = Order(
        name=f"{prenom} {nom}",
        address=adresse,
        items=items,
        total_price=total
    )

    try:
        db.session.add(nouvelle_commande)
        db.session.commit()
    except Exception as e:
        print("Erreur base de données :", e)
        return jsonify({"success": False, "error": str(e)}), 500

    # 📧 Envoi de l'email
    try:
        msg = Message(
            subject="Confirmation de votre commande",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )
        msg.body = f"""Bonjour {prenom},

Merci pour votre commande !

📦 Produits : {items}
💰 Total : {total:.2f}€
📍 Adresse : {adresse}

Nous vous contacterons au {telephone} si nécessaire.

Cordialement,
Ma Boutique
"""
        mail.send(msg)
    except Exception as e:
        print("Erreur d'envoi de mail :", e)

    return jsonify({"success": True})

# ⛔️ Exemption CSRF ici, après la fonction
csrf.exempt(valider_commande)

# 🌍 Fichiers statiques
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

# 🏠 Accueil
@app.route('/')
def accueil():
    return render_template("accueil.html")

@app.route("/afficher_produits")
def afficher_produits():
    if not session.get("user_id"):
        return redirect(url_for("signup"))

    produits = Product.query.all()
    return render_template("produits.html", produits=produits)

@app.route("/panier")
def panier():
    if not session.get("user_id"):
        return redirect(url_for("signup"))

    user_id = session.get('user_id')
    return render_template("panier.html", user_id=user_id)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if not session.get("user_id"):
        return redirect(url_for("signup"))

    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        message = request.form["message"]

        # Enregistrement dans la base de données
        nouveau_message = MessageContact(
            nom=nom,
            prenom=prenom,
            email=email,
            contenu=message
        )
        db.session.add(nouveau_message)
        db.session.commit()

        # Envoi de l'email de confirmation
        try:
            msg = Message(
                subject="Message reçu - Ma Boutique",
                sender=app.config["MAIL_USERNAME"],
                recipients=[email]
            )
            msg.body = f"""Bonjour {prenom},

Nous avons bien reçu votre message :

"{message}"

Nous vous répondrons dans les plus brefs délais.

Cordialement,
L’équipe Ma Boutique
"""
            mail.send(msg)
        except Exception as e:
            print("Erreur d'envoi de mail :", e)

        flash("Votre message a bien été envoyé !", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", user_id=session["user_id"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        motdepasse = request.form["motdepasse"]

        utilisateur = User.query.filter_by(email=email).first()

        if utilisateur and check_password_hash(utilisateur.motdepasse, motdepasse):
            session["user_id"] = utilisateur.id
            return redirect(url_for("afficher_produits"))
        else:
            flash("Email ou mot de passe incorrect.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        nom = request.form["nom"]
        email = request.form["email"]
        motdepasse = generate_password_hash(request.form["motdepasse"])
        adresse = request.form["adresse"]

        if User.query.filter_by(email=email).first():
            flash("Email déjà utilisé.", "warning")
            return redirect(url_for("signup"))

        nouvel_utilisateur = User(nom=nom, email=email, motdepasse=motdepasse, adresse=adresse)
        db.session.add(nouvel_utilisateur)
        db.session.commit()

        session["user_id"] = nouvel_utilisateur.id
        return redirect(url_for("afficher_produits"))

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()  # ou session.pop("user_id", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)

