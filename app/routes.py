from flask import Blueprint, jsonify
from .models import Team, Game
from . import db

main = Blueprint('main', __name__)

@main.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    return jsonify([team.name for team in teams])

def register_blueprints(app):
    app.register_blueprint(main)
