from datetime import datetime
import json
from flask import Flask,render_template,request,redirect,flash,url_for

#Constantes pour les valeurs magiques
MAX_PLACES_PER_CLUB = 12
POINTS_BY_PLACE = 10

def loadClubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']


def loadCompetitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = next(c for c in clubs if c['email'] == request.form['email'][0])
    except StopIteration:
        flash("Sorry, that email was not found.")
        return render_template('welcome.html', club=club, competitions=competitions)

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundClub = next(c for c in clubs if c['name'] == club)
    except StopIteration:
        flash(f"Club '{club}' not found.")
        return render_template('welcome.html', club=club, competitions=competitions)

    try:
        foundCompetition = next(c for c in competitions if c['name'] == competition)
    except StopIteration:
        flash(f"Competition '{competition}' not found.")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    return render_template('booking.html', club=foundClub, competition=foundCompetition),


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    if placesRequired > 12:
        flash(f"Warning: You are trying to book more than 12 places.")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    if placesRequired > int(club['points']):
        flash(f"Warning: You are trying to book more places than available ({club['points']})")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    flash(f'Great-booking complete! You just booked {placesRequired} places for competition "{competition["name"]}"!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/points')
def display_points():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))