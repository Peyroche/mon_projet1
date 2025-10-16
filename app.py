from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, flash, session
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import CSRFProtect
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from validator import validate_signup_data, validate_commande_data, validate_contact_data
from sqlalchemy import text
import psutil
from utils.mail import envoyer_confirmation
import threading
import os

print("🧠 Mémoire utilisée :", psutil.virtual_memory().percent, "%")

# 🔧 Initialisation de l'application
app = Flask(__name__)
app.config.from_object(Config)

# 🔒 Sécurité & extensions
csrf = CSRFProtect(app)
db = SQLAlchemy(app, engine_options=Config.SQLALCHEMY_ENGINE_OPTIONS)
mail = Mail(app)

# ✅ Test de connexion à la base
try:
    with app.app_context():
        db.session.execute(text("SELECT 1"))
    print("✅ Connexion à la base MySQL réussie")
except Exception as e:
    print("❌ Erreur de connexion à la base :", e)

# 🔐 Sécurité des cookies
app.config["SESSION_COOKIE_HTTPONLY"] = True

# 🧱 Modèles SQLAlchemy
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
    image = db.Column(db.String(255))

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
@csrf.exempt
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

    try:
        threading.Thread(
            target=envoyer_confirmation,
            args=(app, mail, email, prenom, message)
        ).start()
    except Exception as e:
        print("Erreur d'envoi de mail (thread contact) :", e)

    return jsonify({"success": True})

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

        # ✅ Envoi du mail dans un thread
        try:
            threading.Thread(
                target=envoyer_confirmation_contact,
                args=(app, mail, email, prenom, message)
            ).start()
        except Exception as e:
            print("Erreur d'envoi de mail (contact) :", e)

        flash("Votre message a bien été envoyé !", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        motdepasse = request.form["motdepasse"]

        utilisateur = User.query.filter_by(email=email).first()

        if utilisateur and check_password_hash(utilisateur.motdepasse, motdepasse):
            session["user_id"] = utilisateur.id
            flash("Connexion réussie !", "success")
            return redirect(url_for("panier"))
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
        return redirect(url_for("panier"))

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/mentions-legales")
def mentions_legales():
    return render_template("mentions_legales.html")

# 🚀 Démarrage Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
