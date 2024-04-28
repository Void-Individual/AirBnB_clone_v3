#!/usr/bin/python3
"""Module to handle the city objects"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models.city import City
from models.state import State
from models import storage


@app_views.route('states/<state_id>/cities', methods=['GET'])
def cities_in_state(state_id):
    """Function to retrieve the cities in a state"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())

    return jsonify(cities)


@app_views.route('cities/<city_id>', methods=['GET'])
def get_city_id(city_id):
    """Function to retrieve a city with its id"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return city.to_dict()


@app_views.route('cities/<city_id>', methods=['DELETE'])
def delete_city_id(city_id):
    """Function to delete a city with it's id"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return {}, 200


@app_views.route('states/<state_id>/cities', methods=['POST'])
def add_city_to_state(state_id):
    """Function to add a new city to a state_id"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        if 'name' not in data:
            abort(400, description="Missing name")
        new_city = City()
        for key, value in data.items():
            setattr(new_city, key, value)
        setattr(new_city, 'state_id', state_id)
        storage.new(new_city)
        storage.save()
        return new_city, 201
