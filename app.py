from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session, send_from_directory
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from validator import validate_signup_data, validate_commande_data, validate_contact_data
from datetime import datetime, timezone
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import secrets
import os

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)
db = SQLAlchemy(app, engine_options=Config.SQLALCHEMY_ENGINE_OPTIONS)

# 🔐 Sécurité des cookies
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True

# Configurer Flask-Mail
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME="tonemail@gmail.com",
    MAIL_PASSWORD="tonmotdepasse"
)
mail = Mail(app)

# Générateur de jeton
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# 🧱 Modèles
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    items = db.Column(db.String(500), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    motdepasse = db.Column(db.String(255), nullable=False)

class MessageContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

with app.app_context():
    db.create_all()

# 📦 Commande
@app.route("/valider_commande", methods=["POST"])
def valider_commande():
    if not request.is_json:
        return jsonify({"success": False, "error": "Requête non JSON"}), 400

    data = request.get_json()
    errors = validate_commande_data(data)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

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
    prenom=prenom,
    address=adresse,
    telephone=telephone,
    email=email,
    items=items,
    total_price=total
    )

    try:
        db.session.add(nouvelle_commande)
        db.session.commit()

    except Exception as e:
        print("Erreur base de données :", e)
        return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": True})

# 🧭 Navigation
@app.route('/')
def accueil():
    return render_template("accueil.html")

@app.route("/afficher_produits")
def afficher_produits():
    return render_template("produits.html")

@app.route("/panier")
def panier():
    if not session.get("user_id"):
        return redirect(url_for("signup"))
    user_id = session.get('user_id')
    return render_template("panier.html", user_id=user_id)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        message = request.form["message"]

        nouveau_message = MessageContact(
            nom=nom,
            prenom=prenom,
            email=email,
            contenu=message
        )
        db.session.add(nouveau_message)
        db.session.commit()

        flash("Votre message a bien été envoyé !", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        motdepasse = generate_password_hash(request.form["motdepasse"])

        if User.query.filter_by(email=email).first():
            flash("Email déjà utilisé.", "warning")
            return redirect(url_for("signup"))

        nouvel_utilisateur = User(nom=nom, prenom=prenom, email=email, motdepasse=motdepasse)
        db.session.add(nouvel_utilisateur)
        db.session.commit()

        session["user_id"] = nouvel_utilisateur.id
        return redirect(url_for("panier"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        motdepasse = request.form["motdepasse"]

        utilisateur = User.query.filter_by(email=email).first()

        if utilisateur and check_password_hash(utilisateur.motdepasse, motdepasse):
            session["user_id"] = utilisateur.id
            return redirect(url_for("panier"))
        else:
            flash("Email ou mot de passe incorrect.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/mentions_legales")
def mentions_legales():
    return render_template("mentions_legales.html")

@app.route("/cgv")
def cgv():
    return render_template("cgv.html")

@app.route("/politique_de_confidentialite")
def politique_de_confidentialite():
    return render_template("politique_de_confidentialite.html")

@app.route("/a_propos")
def a_propos():
    return render_template("a_propos.html")

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(user.email, salt="reset-password")
            reset_url = url_for("reset_password", token=token, _external=True)
            msg = Message("Réinitialisation de mot de passe",
                          sender="tonemail@gmail.com",
                          recipients=[user.email])
            msg.body = f"Pour réinitialiser votre mot de passe, cliquez ici : {reset_url}"
            mail.send(msg)
            flash("Un email de réinitialisation a été envoyé.", "info")
        else:
            flash("Email introuvable.", "danger")
    return render_template("forgot_password.html")

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="reset-password", max_age=3600)  # 1h
    except Exception:
        flash("Lien invalide ou expiré.", "danger")
        return redirect(url_for("forgot_password"))

    user = User.query.filter_by(email=email).first()
    if request.method == "POST":
        new_password = generate_password_hash(request.form["motdepasse"])
        user.motdepasse = new_password
        db.session.commit()
        flash("Mot de passe mis à jour avec succès.", "success")
        return redirect(url_for("login"))

    return render_template("reset_password.html")

# 🚀 Démarrage Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)