from app import app, db, Product

with app.app_context():
    produit = Product.query.filter_by(nom="Savon en boîte").first()
    if produit:
        produit.image = "Savon_en_boite.jpg"
        db.session.commit()
        print("✅ Image mise à jour dans la base.")
    else:
        print("❌ Produit non trouvé.")
