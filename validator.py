import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_signup_data(data):
    errors = []

    if not data.get("nom") or len(data["nom"].strip()) < 2:
        errors.append("Nom trop court ou manquant")

    if not data.get("email") or not is_valid_email(data["email"]):
        errors.append("Email invalide")

    if not data.get("motdepasse") or len(data["motdepasse"]) < 6:
        errors.append("Mot de passe trop court")

    if not data.get("adresse") or len(data["adresse"].strip()) < 5:
        errors.append("Adresse invalide")

    return errors

import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^0[1-9](\d{2}){4}$", phone)

def validate_commande_data(data):
    errors = {}

    required_fields = ["nom", "prenom", "adresse", "telephone", "email", "panier", "total"]
    for field in required_fields:
        if not data.get(field):
            errors[field] = f"Le champ '{field}' est requis."

    if "email" in data and not is_valid_email(data["email"]):
        errors["email"] = "Format d'email invalide."

    if "telephone" in data and not is_valid_phone(data["telephone"]):
        errors["telephone"] = "Format de téléphone invalide."

    try:
        total = float(data.get("total", 0))
        if total < 0:
            errors["total"] = "Le montant total ne peut pas être négatif."
    except (ValueError, TypeError):
        errors["total"] = "Le montant total doit être un nombre."

    if "panier" in data and not isinstance(data["panier"], list):
        errors["panier"] = "Le panier doit être une liste de produits."

    return errors

def validate_contact_data(data):
    errors = {}

    if not data.get("nom") or len(data["nom"].strip()) < 2:
        errors["nom"] = "Nom trop court ou manquant."

    if not data.get("prenom") or len(data["prenom"].strip()) < 2:
        errors["prenom"] = "Prénom trop court ou manquant."

    if not data.get("email") or not is_valid_email(data["email"]):
        errors["email"] = "Email invalide."

    if not data.get("contenu") or len(data["contenu"].strip()) < 10:
        errors["contenu"] = "Le message doit contenir au moins 10 caractères."

    return errors

