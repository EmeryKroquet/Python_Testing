from bs4 import BeautifulSoup

import pytest
from server import app


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


# Test de réservation avec une compétition incorrecte et un club correct
def test_wrong_competition_and_right_club(client):
    competition = "Spring wrongFestival"
    club = "Simply Lift"
    expected_message = 'Something went wrong-please try again'
    response = client.get(f'/book/{competition}/{club}')

    assert response.status_code == 200  # Vérifiez le code d'état HTTP OK
    assert expected_message in extract_error_messages(response)


# Test de réservation avec une compétition correcte et un club incorrect
def test_right_competition_and_wrong_club(client):
    competition = "Spring Festival"
    club = "Simply WrongLift"
    expected_message = 'Something went wrong-please try again'
    response = client.get(f'/book/{competition}/{club}')

    assert response.status_code == 200  # Vérifiez le code d'état HTTP OK
    assert expected_message in extract_error_messages(response)


# Test de réservation avec une compétition et un club incorrects
def test_booking_with_invalid_parameters(client):
    competition = "Spring Festival"
    club = "Simply WrongLift"
    expected_message = 'Something went wrong-please try again'
    response = client.get(f'/book/{competition}/{club}')

    assert response.status_code == 200  # Vérifiez le code d'état HTTP OK
    assert expected_message in extract_error_messages(response)


# Test de la route de réservation
def test_booking_route(client):
    competition = "Spring Festival"
    club = "Simply Lift"
    response = client.get(f'/book/{competition}/{club}')

    assert response.status_code == 200  # Vérifiez le code d'état HTTP OK

# Fonction utilitaire pour extraire les messages d'erreur du contenu HTML
def extract_error_messages(response):
    soup = BeautifulSoup(response.data, features="html.parser")
    error_messages = soup.find_all("li")
    return [message.get_text() for message in error_messages]
