#!/usr/bin/python3
"""Module for the place and amenity object links"""

from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_in_place(place_id):
    """Function to retrieve the amenities ina place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place_amenities = []
    for amenity in place.amenities:
        place_amenities.append(amenity.to_dict())

    return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_of_place(place_id, amenity_id):
    """Function to delete the amenity of a place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if amenity.place_id != place_id:
        abort(404)

    place.amenities.remove(amenity)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Function to link an amenity to a place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
