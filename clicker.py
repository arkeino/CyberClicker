import tkinter as tk
from itertools import cycle
import json
import os

SAVE_FILE = "sauvegarde.txt"

root = tk.Tk()
root.title("Jeu de clic Cyberpunk")
root.configure(bg='#0A0A0A')

argent = 0
multiplicateur = 1
cout_amelioration = 10
dps_total = 0

champions = [
    {"nom": "Hacker", "dps": 1, "niveau": 0, "cout_base": 50, "cout_actuel": 50},
    {"nom": "Cyborg", "dps": 5, "niveau": 0, "cout_base": 200, "cout_actuel": 200},
    {"nom": "Drone", "dps": 10, "niveau": 0, "cout_base": 500, "cout_actuel": 500},
]

images_monstre = [tk.PhotoImage(file=f"monstre_frame_{i}.png") for i in range(1, 4)]
images_cycle = cycle(images_monstre)

def sauvegarder():
    data = {
        "argent": argent,
        "multiplicateur": multiplicateur,
        "cout_amelioration": cout_amelioration,
        "dps_total": dps_total,
        "champions": champions,
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def charger():
    global argent, multiplicateur, cout_amelioration, dps_total, champions
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            argent = data.get("argent", 0)
            multiplicateur = data.get("multiplicateur", 1)
            cout_amelioration = data.get("cout_amelioration", 10)
            dps_total = data.get("dps_total", 0)
            champions = data.get("champions", champions)

def incrementer(event=None):
    global argent
    argent += multiplicateur
    label.config(text=f"Total : {argent}$")
    monstre_label.config(image=next(images_cycle))

def ameliorer():
    global argent, multiplicateur, cout_amelioration
    if argent >= cout_amelioration:
        argent -= cout_amelioration
        multiplicateur += 1
        cout_amelioration += 10
        label.config(text=f"Total : {argent}$")
        amelioration_button.config(text=f"Améliorer (+1$/clic) - Coût : {cout_amelioration}$")
        message.config(text="")
    else:
        message.config(text="Pas assez d'argent pour améliorer!")

def acheter_champion(index):
    global argent, dps_total
    champion = champions[index]
    if argent >= champion["cout_actuel"]:
        argent -= champion["cout_actuel"]
        champion["niveau"] += 1
        dps_total += champion["dps"]
        champion["cout_actuel"] = int(champion["cout_base"] * 1.5 ** champion["niveau"])
        label.config(text=f"Total : {argent}$")
        champions_labels[index].config(text=f"{champion['nom']} (Niveau {champion['niveau']}) - DPS : {champion['dps']} - Coût : {champion['cout_actuel']}$")
        message.config(text="")
        dps_label.config(text=f"DPS total : {dps_total}")
    else:
        message.config(text="Pas assez d'argent pour acheter ce champion!")

def generer_dps():
    global argent
    argent += dps_total
    label.config(text=f"Total : {argent}$")
    root.after(1000, generer_dps)

style_cyberpunk = {"font": ("Courier New", 14), "bg": "#0A0A0A", "fg": "#00FF00", "padx": 10, "pady": 5}
style_bouton = {"font": ("Courier New", 14), "bg": "#1A1A1A", "fg": "#00FFFF", "activebackground": "#333333", "activeforeground": "#00FFFF", "bd": 5, "relief": "raised"}

label = tk.Label(root, text=f"Total : {argent}$", font=("Courier New", 24), bg="#0A0A0A", fg="#00FF00")
label.grid(row=0, column=0, columnspan=2, pady=20)

frame_gauche = tk.Frame(root, bg='#0A0A0A')
frame_gauche.grid(row=1, column=0, padx=20)

frame_gauche.bind("<Button-1>", incrementer)

amelioration_button = tk.Button(frame_gauche, text=f"Améliorer (+1$/clic) - Coût : {cout_amelioration}$", **style_bouton, command=ameliorer)
amelioration_button.pack(pady=20)

dps_label = tk.Label(frame_gauche, text=f"DPS total : {dps_total}", **style_cyberpunk)
dps_label.pack(pady=20)

champions_labels = []
for i, champion in enumerate(champions):
    label_champion = tk.Label(frame_gauche, text=f"{champion['nom']} (Niveau {champion['niveau']}) - DPS : {champion['dps']} - Coût : {champion['cout_actuel']}$", **style_cyberpunk)
    label_champion.pack(pady=5)
    bouton_champion = tk.Button(frame_gauche, text=f"Acheter {champion['nom']}", **style_bouton, command=lambda i=i: acheter_champion(i))
    bouton_champion.pack(pady=5)
    champions_labels.append(label_champion)

frame_droite = tk.Frame(root, bg='#0A0A0A')
frame_droite.grid(row=1, column=1, padx=20)

monstre_label = tk.Label(frame_droite, image=next(images_cycle), bg='#0A0A0A')
monstre_label.pack(pady=20)
monstre_label.bind("<Button-1>", incrementer)

message = tk.Label(root, text="", font=("Courier New", 12), bg="#0A0A0A", fg="#FF00FF")
message.grid(row=2, column=0, columnspan=2, pady=10)

charger()

generer_dps()

root.protocol("WM_DELETE_WINDOW", lambda: (sauvegarder(), root.destroy()))

root.mainloop()