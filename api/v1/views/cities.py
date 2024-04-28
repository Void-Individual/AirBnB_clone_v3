#!/usr/bin/python3
"""Module to handle the city objects"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models.city import City
from models.state import State
from models import storage

@app_views.route('states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def cities_in_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())

    return jsonify(cities)
