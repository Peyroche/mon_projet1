from app import app, db, Product

with app.app_context():
    produits = [
        Product(nom="Savon en boîte", prix=15.0, stock=10, image="Savon_en_boite.jpg"),
        Product(nom="Savon en bouteille", prix=18.0, stock=8, image="Savon_en_bouteille.jpg")
    ]
    db.session.bulk_save_objects(produits)
    db.session.commit()
    print("✅ Produits insérés dans la base.")
