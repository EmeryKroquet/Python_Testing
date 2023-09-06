import json
from flask import Flask, render_template, request, redirect, flash, url_for
import datetime


def loadClubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def loadCompetitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'
app.debug = True

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html', clubs=clubs)  # Correction 9: added clubs as context


@app.route('/showSummary', methods=['POST'])
def showSummary():
    # Correction 2: former code didn't handle wrong email input --> exception handler
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        # Correction 10: former code displayed events in the past --> only future events are displayed
        competitions_to_display = []
        for competition in competitions:
            if datetime.datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S') > datetime.datetime.now():
                competitions_to_display.append(competition)
        return render_template('welcome.html', club=club, competitions=competitions_to_display)
    except IndexError:
        flash('Wrong email. Please try again.')
        return redirect('/')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    # Correction 3: former code didn't handle wrong club or competition --> added an exception handler.
    try:
        found_club = [c for c in clubs if c['name'] == club][0]
        found_competition = [c for c in competitions if c['name'] == competition][0]
        return render_template('booking.html', club=found_club, competition=found_competition)
    except (KeyError, IndexError):
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])

    # Correction 8: sends a message if no places are available anymore
    if int(competition['numberOfPlaces']) == 0:
        flash('Sorry, event is full. You can\'t order places anymore')
        return render_template('welcome.html', club=club, competitions=competitions)

    else:
        # Correction 5: prevents a club from ordering more than 12 places for one event
        if 12 < places_required < int(competition['numberOfPlaces']):
            flash('Sorry you can\'t order more than 12 places for an event')
            return render_template('welcome.html', club=club, competitions=competitions)

        # Correction 7: prevents a club from ordering more places than total available for the competition
        elif places_required > int(competition['numberOfPlaces']):
            flash('Sorry you can\'t order more places than what is available for this competition')
            return render_template('welcome.html', club=club, competitions=competitions)

        # Correction 6: prevents a club from ordering more places than points available in its total
        # Correction 11: added in the condition the fact that a place is worth 3 points
        elif places_required > int(club['points'])/3:
            flash('Sorry you can\'t order more places than you have points available')
            return render_template('welcome.html', club=club, competitions=competitions)

        else:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
            # Correction 4: deduce the number of places purchased from the club's points total
            # Correction 12: the number of points deducted is the number of places times 3
            club['points'] = int(club['points']) - (places_required*3)
            flash(f'Great-booking complete! {places_required} places booked.')
            return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


# Correction 1: code below was missing --> server couldn't be launched
if __name__ == "__main__":
    app.run()