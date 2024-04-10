import matplotlib
matplotlib.use('Agg')  # Utiliser un backend non interactif

from flask import Flask, render_template
import requests
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

def get_api_data():
    url = "https://api.steambase.io/games?sortBy=players&sortDirection=1&skip=0&take=10"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_custom_chart(games):
    # Utiliser les données de l'API pour générer le graphique
    values = [game['current_players'] for game in games]
    labels = [game['name'] for game in games]
    
    # Créer le graphique
    fig, ax = plt.subplots()
    
    # Créer un bar chart basé sur les données de l'API
    ax.bar(labels, values)
    
    ax.set(xlim=(0, len(labels)), xticks=np.arange(len(labels)),
           ylim=(0, max(values)*1.2))
    
    # Ajouter les labels
    ax.set_xticklabels(labels, rotation=45, ha="right")
    
    # Ajouter les valeurs au-dessus des barres
    for i, v in enumerate(values):
        ax.text(i, v + max(values)*0.01, str(v), ha='center', va='bottom')
    
    # Sauvegarder le graphique en tant qu'image PNG
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.close(fig)  # Fermer la figure pour libérer la mémoire
    return f"data:image/png;base64,{data}"

@app.route('/')
def index():
    api_data = get_api_data()
    if api_data:
        games = api_data
        custom_chart_data = create_custom_chart(games)
        return render_template('index.html', games=games, custom_chart_data=custom_chart_data)
    else:
        return "Erreur lors de la récupération des données de l'API"

if __name__ == '__main__':
    app.run(debug=True)
