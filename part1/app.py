import tkinter as tk
from tkinter import messagebox, Menu, colorchooser, simpledialog, font
import sqlite3
import os
from db.insert_sqlite import inserer_donnees_sqlite
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Smartphones Auchan")
root.geometry("900x700")

# Police par défaut
current_font_family = "Arial"
current_font_size = 12

def appliquer_police():
    f = (current_font_family, current_font_size)
    result_label.config(font=f)
    btn_moyenne.config(font=f)
    btn_graph.config(font=f)

# Zone de texte pour afficher les résultats
result_label = tk.Label(root, text="", font=(current_font_family, current_font_size))
result_label.pack(pady=20)

# --- FONCTIONS ---

def afficher_moyenne_rating():
    try:
        conn = sqlite3.connect("db/auchan.db")
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(rating) FROM smartphones")
        moyenne = cursor.fetchone()[0]
        conn.close()

        if moyenne is not None:
            result_label.config(text=f"Note moyenne des smartphones : {round(moyenne, 2)} / 5")
        else:
            result_label.config(text="Aucune donnée disponible.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la requête SQL : {e}")

def supprimer_donnees():
    try:
        conn = sqlite3.connect("db/auchan.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM smartphones")
        conn.commit()
        conn.close()
        messagebox.showinfo("Succès", "Données supprimées avec succès.")
        result_label.config(text="")
        # Supprimer aussi les graphiques affichés
        for widget in root.pack_slaves():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")

def telecharger_donnees():
    success = inserer_donnees_sqlite()
    if success:
        messagebox.showinfo("Succès", "Données téléchargées et enregistrées dans la base.")
    else:
        messagebox.showwarning("Annulé", "Téléchargement annulé ou échoué.")

def afficher_graphique():
    try:
        conn = sqlite3.connect("db/auchan.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                UPPER(SUBSTR(title, 1, INSTR(title, ' ') - 1)) AS marque,
                ROUND(AVG(rating), 2) as moyenne_note
            FROM smartphones
            WHERE rating != 'N/A'
            GROUP BY marque
            ORDER BY moyenne_note DESC
        """)
        result = cursor.fetchall()
        conn.close()

        if not result:
            messagebox.showinfo("Info", "Aucune donnée pour générer le graphique.")
            return

        marques = [row[0] for row in result]
        notes = [row[1] for row in result]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(marques, notes, color="skyblue")
        ax.set_title("Note moyenne par marque")
        ax.set_xlabel("Marque")
        ax.set_ylabel("Note Moyenne")
        ax.set_ylim(0, 5)

        # Supprimer les anciens graphiques s'il y en a
        for widget in root.pack_slaves():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'affichage du graphique : {e}")

def choisir_couleur():
    couleur = colorchooser.askcolor(title="Choisir une couleur de fond")
    if couleur[1]:
        root.config(bg=couleur[1])
        result_label.config(bg=couleur[1])
        btn_moyenne.config(bg=couleur[1])
        btn_graph.config(bg=couleur[1])

def choisir_police():
    global current_font_family
    # Liste simple de polices courantes
    polices = ["Arial", "Helvetica", "Times New Roman", "Courier New", "Comic Sans MS"]
    
    # Demande à l'utilisateur de choisir la police
    choix = simpledialog.askstring("Choisir police", f"Police disponible :\n{', '.join(polices)}\n\nEntrez le nom exact de la police :")
    if choix and choix in polices:
        current_font_family = choix
        appliquer_police()
    else:
        messagebox.showwarning("Police invalide", "Police non reconnue ou annulation.")

# --- MENU ---

menu_bar = Menu(root)

menu_data = Menu(menu_bar, tearoff=0)
menu_data.add_command(label="Télécharger les données", command=telecharger_donnees)
menu_data.add_command(label="Effacer la base de données", command=supprimer_donnees)
menu_bar.add_cascade(label="Base de données", menu=menu_data)

menu_options = Menu(menu_bar, tearoff=0)
menu_options.add_command(label="Changer la couleur de fond", command=choisir_couleur)
menu_options.add_command(label="Changer la police", command=choisir_police)
menu_bar.add_cascade(label="Options", menu=menu_options)

root.config(menu=menu_bar)

# --- BOUTONS ---

btn_moyenne = tk.Button(root, text="Afficher la moyenne des notes", command=afficher_moyenne_rating, font=(current_font_family, current_font_size))
btn_moyenne.pack(pady=10)

btn_graph = tk.Button(root, text="Afficher le graphique", command=afficher_graphique, font=(current_font_family, current_font_size))
btn_graph.pack(pady=10)

# Boucle principale
root.mainloop()
