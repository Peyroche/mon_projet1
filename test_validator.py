import pytest
from validator import validate_commande_data

def test_commande_valide():
    data = {
        "nom": "Jean",
        "prenom": "Dupont",
        "adresse": "12 rue des Lilas",
        "telephone": "0612345678",
        "email": "jean@example.com",
        "panier": [{"produit": "Livre", "prix": 15}],
        "total": 15.0
    }
    errors = validate_commande_data(data)
    assert errors == {}

def test_commande_email_invalide():
    data = {
        "nom": "Jean",
        "prenom": "Dupont",
        "adresse": "12 rue des Lilas",
        "telephone": "0612345678",
        "email": "jeanexample.com",  # ❌ email invalide
        "panier": [{"produit": "Livre", "prix": 15}],
        "total": 15.0
    }
    errors = validate_commande_data(data)
    assert "email" in errors

def test_commande_total_negatif():
    data = {
        "nom": "Jean",
        "prenom": "Dupont",
        "adresse": "12 rue des Lilas",
        "telephone": "0612345678",
        "email": "jean@example.com",
        "panier": [{"produit": "Livre", "prix": 15}],
        "total": -5.0  # ❌ total négatif
    }
    errors = validate_commande_data(data)
    assert "total" in errors

def test_commande_panier_non_liste():
    data = {
        "nom": "Jean",
        "prenom": "Dupont",
        "adresse": "12 rue des Lilas",
        "telephone": "0612345678",
        "email": "jean@example.com",
        "panier": "Livre",  # ❌ pas une liste
        "total": 15.0
    }
    errors = validate_commande_data(data)
    assert "panier" in errors
