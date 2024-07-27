from . import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    abbreviation = db.Column(db.String(10))
    city = db.Column(db.String(255))

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    home_team_score = db.Column(db.Integer)
    away_team_score = db.Column(db.Integer)
