#!/usr/bin/python3
"""Module for the places objects"""

from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_in_city(city_id):
    """Function to retrieve the places in a city object"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = storage.all(Place).values()
    city_places = []
    for place in places:
        if place.city_id == city_id:
            city_places.append(place.to_dict())

    return jsonify(city_places)


@app_views.route('/places/<id>', methods=['GET'], strict_slashes=False)
def get_place(id):
    """Function to retrieve a place object with id"""

    place = storage.get(Place, id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<id>', methods=['DELETE'], strict_slashes=False)
def delete_place(id):
    """Function to delete a place"""

    place = storage.get(Place, id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Function to creaate a new place in a city"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    if 'name' not in data:
        abort(400, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<id>', methods=['PUT'], strict_slashes=False)
def update_place(id):
    """Function to update the details of a place"""

    place = storage.get(Place, id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a valid JSON')

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
