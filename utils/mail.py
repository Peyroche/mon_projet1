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



