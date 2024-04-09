from flask import Flask, render_template
import requests
import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt  # Ajoutez cette ligne pour importer plt

app = Flask(__name__)

def get_api_data():
    url = "https://api.steambase.io/games?sortBy=players&sortDirection=1&skip=0&take=10"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_pie_chart(games):
    fig = Figure()
    ax = fig.subplots()
    
    # Préparation des données pour le graphique
    # Supposons que vous voulez afficher le nombre de joueurs en ligne pour chaque jeu
    # Vous pouvez ajuster cela en fonction des données réelles que vous souhaitez afficher
    values = [game['current_players'] for game in games]
    labels = [game['name'] for game in games]
    
    # Génération des couleurs pour chaque segment du graphique
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(values)))
    
    # Création du graphique de type pie chart
    ax.pie(values, labels=labels, colors=colors, radius=3, center=(4, 4),
           wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, autopct='%1.1f%%')
    
    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
           ylim=(0, 8), yticks=np.arange(1, 8))
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64,{data}"


@app.route('/')
def index():
    api_data = get_api_data()
    if api_data:
        games = api_data
        pie_chart_data = create_pie_chart(games)
        return render_template('index.html', games=games, pie_chart_data=pie_chart_data)
    else:
        return "Erreur lors de la récupération des données de l'API"


if __name__ == '__main__':
    app.run(debug=True)