#!/usr/bin/python3
"""View of States"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    states = storage.all('State')
    the_states = []
    for state in states.values():
        the_states.append(state.to_dict())
    return jsonify(the_states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def a_state():
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_state(state_id=None):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state(state_id=None):
    """Create a state"""

    httpbody = request.get_json()
    if not httpbody:
        abort(400, description="Not a JSON")
    if "name" not in httpbody:
        abort(400, description="Missing name")

    state = State(**httpbody)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id=None):
    """Updates a State object"""
    httpbody = request.get_json()
    if not httpbody:
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if state:
        for key, value in httpbody.items():
            setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
    abort(404)
