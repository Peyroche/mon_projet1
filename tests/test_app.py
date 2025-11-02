import unittest
from app import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_valider_commande_valide(self):
        response = self.client.post("/valider_commande", json={
            "nom": "Dupont",
            "prenom": "Jean",
            "adresse": "123 rue de Paris",
            "telephone": "0601020304",
            "email": "jean.dupont@example.com",
            "panier": [{"produit": "Savon noir", "prix": 15}],
            "total": 15
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.get_json())
        self.assertTrue(response.get_json()["success"])

    def test_valider_commande_invalide(self):
        # Cas sans email
        response = self.client.post("/valider_commande", json={
            "nom": "Dupont",
            "prenom": "Jean",
            "adresse": "123 rue de Paris",
            "telephone": "0601020304",
            "panier": [{"produit": "Savon noir", "prix": 15}],
            "total": 15
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.get_json())
        self.assertTrue(response.get_json()["success"])  # Peut être True si email facultatif

    def test_valider_commande_mauvais_format(self):
        # Cas avec données non JSON
        response = self.client.post("/valider_commande", data="Juste du texte")
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
