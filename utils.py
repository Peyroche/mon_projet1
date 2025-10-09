from flask_mail import Message
from threading import Thread

def envoyer_confirmation(app, mail, email, prenom, items, total, adresse, telephone):
    def send_async_email():
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

    Thread(target=send_async_email).start()