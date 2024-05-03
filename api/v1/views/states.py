#!/usr/bin/python3
"""Module to handle all the state objects"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Function to retireve all states"""

    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    print('Check 0')
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """Function to retrieve a state with it's id"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state_id(state_id):
    """Function to delete a state with it's id"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        state.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def put_state():
    """Function to create a state with certain details"""

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_in_state(state_id):
    """Function to change certain details in a state"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'updated_at', 'created_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
