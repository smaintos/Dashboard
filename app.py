from flask import Flask, render_template
import requests

app = Flask(__name__)

# Fonction pour récupérer les données de l'API
def get_api_data():
    url = "https://api.steambase.io/games?sortBy=players&sortDirection=1&skip=0&take=20"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Route pour la page d'accueil
@app.route('/')
def index():
    api_data = get_api_data()
    if api_data:
        games = api_data  # api_data est déjà une liste
        return render_template('index.html', games=games)
    else:
        return "Erreur lors de la récupération des données de l'API"


if __name__ == '__main__':
    app.run(debug=True)
