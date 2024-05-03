#!/usr/bin/python3
"""Module for the places objects"""

from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from flask import abort, jsonify, request
from api.v1.views import app_views
import requests
import json
from os import getenv


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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Function to retrieve all place objects depending on json request"""

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    saved_places = storage.all(Place).values()
    if not data or (not data.get('states') and not data.get('cities') and not
                    data.get('amenitites')):
        return jsonify([place.to_dict() for place in saved_places])

    matched_places = []
    if data.get('states'):
        states = [storage.get(State, id) for id in data.get('states')]
        for state in states:
            for city in state.cities:
                for place in city.places():
                    matched_places.append(place)

    if data.get('cities'):
        cities = [storage.get(City, id) for id in data.get('cities')]
        for city in cities:
            for place in city.places:
                if place not in matched_places:
                    matched_places.append(place)

    if not matched_places:
        matched_places = saved_places

    if data.get('amenities'):
        amenities = [storage.get(Amenity, id) for id in data.get('amenities')]
        x = 0
        limit = len(amenities)
        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        first_url = "http://0.0.0.0:{}/api/v1/places/".format(port)

        while x < limit:
            place = matched_places[x]
            url = first_url + '{}/amenities'
            req = url.format(place.id)
            response = requests.get(req)
            resp = json.loads(response)
            p_amenities = [storage.get(Amenity, obj[id]) for obj in resp]
            for amenity in p_amenities:
                if amenity not in amenities:
                    matched_places.pop(x)
                    x -= 1
                    limit -= 1
                    break
            x += 1
    return jsonify([place.to_dict() for place in matched_places])


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
