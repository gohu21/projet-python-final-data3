import sqlite3
import pandas as pd
import os
import json

def inserer_donnees_sqlite():
    # Charger les données JSON
    json_path = "./auchan_smartphones.json"
    if not os.path.exists(json_path):
        print("Fichier JSON introuvable.")
        return False

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conn = sqlite3.connect("db/auchan.db")
    cursor = conn.cursor()

    # Création de la table si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smartphones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price TEXT,
            seller TEXT,
            rating REAL
        )
    """)

    # Vérifier si la table contient déjà des données
    cursor.execute("SELECT COUNT(*) FROM smartphones")
    count = cursor.fetchone()[0]

    if count > 0:
        from tkinter import messagebox
        reponse = messagebox.askyesno("Base non vide", "La base contient déjà des données. Écraser ?")
        if reponse:
            cursor.execute("DELETE FROM smartphones")
        else:
            conn.close()
            return False

    # Insertion des données JSON dans la base SQLite
    for item in data:
        title = item.get("title", "N/A")
        price = item.get("price", "N/A")
        seller = item.get("seller", "N/A")
        try:
            rating = float(item.get("rating", 0))
        except:
            rating = 0.0
        cursor.execute("INSERT INTO smartphones (title, price, seller, rating) VALUES (?, ?, ?, ?)",
                       (title, price, seller, rating))

    conn.commit()
    conn.close()
    return True
