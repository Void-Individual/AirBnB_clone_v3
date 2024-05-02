#!/usr/bin/python3
"""Module for the places objects"""

from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Function to retrieve all place objects depending on json request"""

    try:
        data = request.get_json()
        saved_places = storage.all(Place).values()
        saved_cities = storage.all(City).values()
        if data is None or (not data['states'] and not data['cities']
                             and not data['amenities']):
            return jsonify([place.to_dict() for place in saved_places])

        matched_places = []
        if data.get('states'):
            state_ids = data['states']
            cities_in_states = [city for city in saved_cities if city.state_id in state_ids]
            city_ids = [city.id for city in cities_in_states]
            state_places = [place for place in saved_places if place.city_id in city_ids]
            matched_places = state_places

        if data.get('cities'):
            city_ids = data['cities']
            city_places = [place for place in saved_places if place.city_id in city_ids]

        for place in city_places:
            if place not in matched_places:
                matched_places.append(place)

        if data.get('amenities'):
            amenity_ids = data['amenities']
            place_with_amenities = [place for place in saved_places if place.amenity_ids == amenity_ids]
            if matched_places:
                matching_places = [place.to_dict() for place in matched_places if place in place_with_amenities]
            else:
                matching_places = [place.to_dict() for place in place_with_amenities]
            return jsonify(matching_places)
        else:
            matching_places = [place.to_dict() for place in matched_places]
            return jsonify(matching_places)
    except Exception:
        abort(400, 'Not a JSON')


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
