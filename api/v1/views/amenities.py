#!/usr/bin/python3
"""Module for the amenities object"""

from flask import jsonify, abort, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Function to retrieve all amenity objects"""

    amenites = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenites)


@app_views.route('/amenities/<id>', methods=['GET'], strict_slashes=False)
def get_amenity(id):
    """Function to retrieve a specific amenity"""

    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities//<id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(id):
    """Function to delete an amenity object"""

    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Function to create a new amenity object"""

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    if 'name' not in data:
        abort(400, 'Missing name')

    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<id>', methods=['PUT'], strict_slashes=False)
def update_amenity(id):
    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 201
