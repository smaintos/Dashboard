import matplotlib
matplotlib.use('Agg') 

from flask import Flask, render_template, request
import requests
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

app = Flask(__name__)

def get_api_data():
    game_limit = request.args.get('gameLimit', default=10, type=int)
    url = f"https://api.steambase.io/games?sortBy=players&sortDirection=1&skip=0&take={game_limit}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_custom_chart(games):
    values = [game['current_players'] for game in games]
    labels = [game['name'] for game in games]
    
    fig, ax = plt.subplots()
    
    ax.barh(labels, values, color='green')
    
    ax.set(xlabel='Nombre de joueurs en ligne', ylabel='Jeux')
    
    for i, (v, label) in enumerate(zip(values, labels)):
        ax.text(v + max(values)*0.01, i, str(v), ha='left', va='center')
    
    ax.invert_yaxis()
    
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.close(fig)  
    return f"data:image/png;base64,{data}"

def create_disonnected_chart(games):
    games_sorted = sorted(games, key=lambda x: x['disconnected_players'])
    
    games_sorted = list(reversed(games_sorted))
    
    values = [game['disconnected_players'] for game in games_sorted]
    labels = [game['name'] for game in games_sorted]
    
    fig, ax = plt.subplots()
    
    ax.barh(labels, values, color='red')
    
    ax.set(xlabel='Nombre de joueurs déconnectés', ylabel='Jeux')
    
    ax.set_xlim([0, max(values)])  
    
    for i, (v, label) in enumerate(zip(values, labels)):
        ax.text(v + max(values)*0.01, i, str(v), ha='left', va='center')
    
    ax.invert_yaxis()
    

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.close(fig)  
    return f"data:image/png;base64,{data}"


def calculate_disconnected_players(game):
    community_members = game.get('community_hub_members')
    current_players = game.get('current_players')
    if community_members is not None and current_players is not None:
        return community_members - current_players
    else:
        return 0  


@app.route('/')
def index():
    api_data = get_api_data()
    if api_data:
        games = api_data
        for game in games:
            game['disconnected_players'] = calculate_disconnected_players(game)  
        custom_chart_data = create_custom_chart(games)
        disconnected_chart_data = create_disonnected_chart(games)
        return render_template('index.html', games=games, custom_chart_data=custom_chart_data , disconnected_chart_data=disconnected_chart_data) 
    
    else:
        return "Erreur lors de la récupération des données de l'API"

if __name__ == '__main__':
    app.run(debug=True)
