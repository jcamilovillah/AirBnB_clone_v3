#!/usr/bin/python3
"""RestFul API actions City
"""

from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_by_state(state_id=None):
    """Retrieves the list of all City objects
    """
    state = storage.get('State', state_id)
    list_cities = []
    if state:
        for city in state.cities:
            list_cities.append(city.to_dict())
        return jsonify(list_cities)
    else:
        abort(404)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def show_city(city_id=None):
    """Retrieves the list of all City objects
    """
    city = storage.get('City', city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """Deletes a city object
    """
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_cities(state_id=None):
    """Creates a city
    """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in dict_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_city = City(**dict_json)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities(city_id=None):
    """Updates a city object
    """
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    city = storage.get('City', city_id)
    if city:
        for key, value in dict_json.items():
            setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
    else:
        return abort(404)
