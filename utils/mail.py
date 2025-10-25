from flask_mail import Message

def envoyer_confirmation(app, mail, email, prenom, message):
    try:
        with app.app_context():
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
L’équipe MD Consulting
"""
            mail.send(msg)
    except Exception as e:
        print("Erreur SMTP contact :", e)


def envoyer_confirmation_commande(app, mail, email, prenom, items, total, adresse, telephone):
    try:
        with app.app_context():
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


__all__ = ["envoyer_confirmation", "envoyer_confirmation_commande"]
