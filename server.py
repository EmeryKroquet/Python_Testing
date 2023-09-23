from datetime import datetime
import json
from flask import Flask, render_template, request, redirect, flash, url_for, Response


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club_email = request.form['email']

    # club not found
    if club_email not in [club['email'] for club in clubs]:
        return Response(response="<p>Sorry, that email wasn't found.</p>", status=404)

    club = [club for club in clubs if club['email'] == club_email][0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:

        # check if competition already done
        if datetime.fromisoformat(foundCompetition['date']) < datetime.now():
            flash(f"Warning : competition {foundCompetition['name']} is closed. Past competition.")
            return render_template('welcome.html', club=foundClub, competitions=competitions), 400

        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # check for 12 places limit of purchase
    if placesRequired > 12:
        flash(f"Warning : you are trying to book more 12 places.")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    # check for available club points
    if placesRequired > int(club['points']):
        flash(f"Warning : you are trying to book more places than available ({club['points']})")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    flash(f'Great-booking complete! You just booked {placesRequired} places for competition "{competition["name"]}"!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/showClubsSummary')
def showClubsSummary():
    return render_template('clubs.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


# CUSTOM TEMPLATES FILTERS
@app.template_filter('to_date')
def to_date_filer(iso_date):
    return datetime.fromisoformat(iso_date)


@app.template_filter('is_future')
def is_future_filer(date):
    return date > datetime.now()