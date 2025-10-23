from flask_mail import Message

with app.app_context():
    envoyer_confirmation(app, mail, "ton_email_test@example.com", "Test", "Produit X", 10.0, "Adres")

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
