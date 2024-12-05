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
def watch_list():
    """
    Page principale listant toutes les montres disponibles
    """
    try:
        # Récupérer les montres depuis l'API
        response = requests.get(f'{API_BASE_URL}/watches/')
        watches = response.json()

        # Préparer les montres avec une image principale
        for watch in watches:
            primary_image = next((img['image_url'] for img in watch['images'] if img['is_primary']), None)
            watch['primary_image'] = primary_image or '/static/images/default-watch.jpg'

        return render_template('watch_list.html', watches=watches)
    except requests.exceptions.RequestException:
        # Gestion des erreurs de requête API
        return render_template('error.html', message="Impossible de charger les montres"), 500


@app.route('/watch/<int:watch_id>')
def watch_detail(watch_id):
    """
    Page de détail pour une montre spécifique
    """
    try:
        # Récupérer les détails de la montre depuis l'API
        response = requests.get(f'{API_BASE_URL}/watches/{watch_id}')

        if response.status_code == 404:
            abort(404)

        watch = response.json()

        # Préparer les images
        watch['images'] = watch.get('images', [])

        return render_template('watch_detail.html', watch=watch)
    except requests.exceptions.RequestException:
        return render_template('error.html', message="Erreur de chargement des détails"), 500


@app.errorhandler(404)
def page_not_found(e):
    """
    Gestion personnalisée des erreurs 404
    """
    return render_template('error.html', message="Page non trouvée"), 404


if __name__ == '__main__':
    app.run(debug=True)