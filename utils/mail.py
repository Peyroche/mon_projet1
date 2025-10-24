from flask_mail import Message

def envoyer_confirmation(app, mail, email, prenom, items, total, adresse, telephone):
    with app.app_context():
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
MD Consulting
"""
            mail.send(msg)
        except Exception as e:
            print("Erreur d'envoi de mail :", e)

def envoyer_confirmation_contact(app, mail, email, prenom, message):
    with app.app_context():
        try:
            msg = Message(
                subject="Confirmation de votre message",
                sender=app.config["MAIL_USERNAME"],
                recipients=[email]
            )
            msg.body = f"""Bonjour {prenom},

Merci pour votre message :

📝 "{message}"

Nous vous répondrons dans les plus brefs délais.

Cordialement,
MD Consulting
"""
            mail.send(msg)
        except Exception as e:
            print("Erreur d'envoi de mail (contact) :", e)
