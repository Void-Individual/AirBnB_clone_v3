#!/usr/bin/python3
"""Module to handle all the state objects"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('states')
def get_states():
    """Function to retireve all states"""

    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('states/<state_id>', methods=['GET'])
def get_state_id(state_id):
    """Function to retrieve a state with it's id"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        return state.to_dict()


@app_views.route('states/<state_id>',
                 methods=['DELETE'])
def delete_state_id(state_id):
    """Function to delete a state with it's id"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return {}, 200


@app_views.route('states', methods=['POST'])
def put_state():
    """Function to create a state with certain details"""

    data = request.get_json()
    if not data:
        abort(404, description='Not a JSON')
    if 'name' not in data:
        abort(404, description='Missing name')
    new_state = State(data)
    for key, value in data.items():
        setattr(new_state, key, value)
    storage.new(new_state)
    storage.save()
    return new_state.to_dict(), 201


@app_views.route('states/<state_id>', methods=['PUT'])
def put_in_state(state_id):
    """Function to change certain details in a state"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(404, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'updated_at', 'created_at']:
            setattr(state, key, value)
            state.save()
    storage.save()
    return state.to_dict(), 200
