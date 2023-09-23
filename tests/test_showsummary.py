from bs4 import BeautifulSoup
import pytest
from server import app


# Fixture pour créer un client de test
@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client

# Données de test pour les clubs
clubs = [
    {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    },
    {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    },
    {
        "name": "She Lifts",
        "email": "kate@shelifts.co.uk",
        "points": "12"
    }
]


# Test de la route /showSummary avec un e-mail valide
def test_show_summary_with_valid_email(client):
    # Données du formulaire de test
    form_data = {'email': 'admin@irontemple.com'}

    # Texte attendu dans la réponse
    expected_text = 'Welcome, admin@irontemple.com'

    # Envoyer une requête POST à la route /showSummary
    response = client.post('/showSummary', data=form_data)

    # Analyser la réponse avec BeautifulSoup
    soup = BeautifulSoup(response.data, features="html.parser")
    soup_content = soup.find_all("h2")

    # Vérifier que le texte attendu est présent dans la réponse
    assert expected_text in soup_content[0].get_text()

    # Vérifier que le code d'état HTTP est OK (200)
    assert response.status_code == 200


# Test de la route /showSummary avec un e-mail invalide
def test_show_summary_with_invalid_email(client):
    # Données du formulaire de test
    form_data = {'email': 'test@test.com'}

    # Texte attendu dans la réponse
    expected_text = 'You should be redirected automatically to the target URL: '

    # Envoyer une requête POST à la route /showSummary
    response = client.post('/showSummary', data=form_data)

    # Analyser la réponse avec BeautifulSoup
    soup = BeautifulSoup(response.data, features="html.parser")
    soup_content = soup.find_all("p")

    # Vérifier que le texte attendu est présent dans la réponse
    assert expected_text in soup_content[0].get_text()

    # Vérifier que le code d'état HTTP est une redirection (302)
    assert response.status_code == 302
