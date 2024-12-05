import os
from flask import Flask, render_template, abort
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Configuration de l'API
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

@app.route('/')
def home():
    """
    Page d'accueil
    """
    return render_template('index.html')
@app.errorhandler(404)
def page_not_found(e):
    """
    Gestion personnalisée des erreurs 404
    """
    return render_template('error.html', message="Page non trouvée"), 404


if __name__ == '__main__':
    app.run(debug=True)