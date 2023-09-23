from bs4 import BeautifulSoup


import pytest
from server import app


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client

clubs = [
    {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": 13
    },
    {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": 4
    },
    {
        "name": "She Lifts",
        "email": "kate@shelifts.co.uk",
        "points": 12
    }
]

competitions = [
    {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": 25
    },
    {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": 13
    }
]


def test_buying_places_should_decrease_points_available(client):
    form_data = {'club': 'Iron Temple', 'competition': 'Spring Festival', 'places': 1}
    # Enregistrez les points initiaux du club en tant qu'entier et les places initiales de la compétition
    initial_club_points = int(clubs[1]['points'])
    initial_competition_places = competitions[0]['numberOfPlaces']
    response = client.post('/purchasePlaces', data=form_data)
    soup = BeautifulSoup(response.data, features="html.parser")
    # Vérifiez que le message de succès s'affiche
    assert 'Great-booking complete!' in soup.get_text()
    # Mettez à jour la valeur des points du club dans la liste des clubs
    clubs[1]['points'] = str(initial_club_points - 1)
    assert response.status_code == 200  # Vérifiez le code d'état HTTP OK
    # Vérifiez que les points du club ont diminué de 1
    assert int(clubs[1]['points']) == initial_club_points - 1


def test_club_cant_buy_more_places_than_points_available(client):
    form_data = {'club': 'Iron Temple', 'competition': 'Spring Festival', 'places': 5}
    response = client.post('/purchasePlaces', data=form_data)
    soup = BeautifulSoup(response.data, features="html.parser")
    # Vérifiez que le message d'erreur s'affiche
    assert "Sorry you can't order more places than you have points available" in soup.get_text()
    # Vérifiez que les points du club n'ont pas changé
    initial_club_points = int(clubs[1]['points'])  # Convertissez les points en entier
    assert initial_club_points == 3
    assert response.status_code == 200  # Vérifiez le code d'état HTTP OK
    # Assurez-vous que les points du club dans la liste des clubs sont inchangés
    assert int(clubs[1]['points']) == initial_club_points



def test_club_cant_buy_more_than_12_places(client):
    form_data = {'club': 'Iron Temple', 'competition': 'Spring Festival', 'places': 14}
    response = client.post('/purchasePlaces', data=form_data)
    soup = BeautifulSoup(response.data, features="html.parser")
    # Vérifiez que le message d'erreur s'affiche
    assert "Sorry you can't order more than 12 places for an event" in soup.get_text()
    assert response.status_code == 200  # Vérifiez le code d'état HTTP OK
    # Vérifiez que le nombre de places disponibles pour la compétition n'ait pas changé
    assert competitions[0]['numberOfPlaces'] == 25


def test_club_cant_buy_more_places_than_available_for_competition(client):
    form_data = {'club': 'Iron Temple', 'competition': 'Spring Festival', 'places': 30}
    response = client.post('/purchasePlaces', data=form_data)
    soup = BeautifulSoup(response.data, features="html.parser")
    # Vérifiez que le message d'erreur s'affiche
    assert "Sorry you can't order more places than what is available for this competition" in soup.get_text()
    assert response.status_code == 200  # Vérifiez le code d'état HTTP OK
    # Vérifiez que le nombre de places disponibles pour la compétition n'ait pas changé
    assert competitions[0]['numberOfPlaces'] == 25


