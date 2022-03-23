import json
from flask import Flask,render_template,request,redirect,flash,url_for


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
def index(error=None):
    return render_template('index.html', error_message=error)

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]    
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        return index("Sorry, that email is not valid")
    


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    club_points = int(club["points"])
    # competition_date = parse(competition["date"])
    try:
        ordered_spots = int(request.form["places"])
    except ValueError:
        ordered_spots = 0
        
    available_spots = int(competition["numberOfPlaces"])
    
    if club_points < ordered_spots:
        flash(f"Error: unsufficient points to book {ordered_spots} places")
    elif ordered_spots > available_spots:        
        flash(f"Error: there is only {available_spots} places available. You asked for {ordered_spots}")
    else:
        competition["numberOfPlaces"] = available_spots - ordered_spots
        club["points"] = club_points - ordered_spots
        flash("Great-booking complete!")

    return render_template("welcome.html", club=club, competitions=competitions)

    
    


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))