#!/usr/bin/python3
"""RestFul API actions Amenity
"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_all(city_id=None):
    """Retrieves the list of all Place objects
    """
    city = storage.get('City', city_id)
    places_list = []
    if city:
        for place in city.places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def places_id(place_id=None):
    """Retrieves the list of all Place objects
    """
    place = storage.get('Place', place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Deletes a place object
    """
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_places(city_id=None):
    """Creates a place
    """
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in dict_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    cities = storage.get('City', city_id)
    users = storage.get('User', dict_json['user_id'])
    if cities and users:
        new_place = Place(**dict_json)
        new_place.city_id = cities.id
        storage.new(new_place)
        storage.save()
        return make_response(jsonify(new_place.to_dict()), 201)
    return abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_places(place_id=None):
    """Updates a place object
    """
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    places_obj = storage.get('Place', place_id)
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    if places_obj:
        for key, value in dict_json.items():
            if key not in ignore:
                setattr(places_obj, key, value)
        storage.save()
        return make_response(jsonify(places_obj.to_dict()), 200)
    else:
        return abort(404)
