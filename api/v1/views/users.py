#!/usr/bin/python3
"""Module for the user objects"""

from flask import abort, jsonify, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """function to retrieve all tghe user objects"""

    users = storage.all(User).values()
    all = [user.to_dict() for user in users]
    return jsonify(all)


@app_views.route('/users/<id>', methods=['GET'], strict_slashes=False)
def get_user(id):
    """Function to retrieve a user with id"""

    user = storage.get(User, id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<id>', methods=['DELETE'], strict_slashes=False)
def delete_user(id):
    """Function to delete a user object with its id"""

    user = storage.get(User, id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Function to create a new user"""

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    if 'email' not in data:
        abort(400, 'Missing email')

    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<id>', methods=['PUT'], strict_slashes=False)
def update_user(id):
    """Function to update the details of a user"""

    user = storage.get(User, id)
    if user is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
