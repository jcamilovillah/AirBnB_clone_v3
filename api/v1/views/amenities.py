#!/usr/bin/python3
"""RestFul API actions Amenity
"""
from models.amenity import Amenity
from models import storage
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Retrieves all amenities
    """
    amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def one_amenity(amenity_id=None):
    """Retrieve an amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id=None):
    """Delete amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """Create an amenity
    """
    dict_json = request.get_json()
    if not dict_json:
        abort(400, description="Not a JSON")
    if 'name' not in dict_json:
        abort(400, description="Missing name")

    new_amenity = Amenity(**dict_json)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenities(amenity_id=None):
    """Update an amenity
    """
    dict_json = request.get_json()
    if not dict_json:
        abort(400, description="Not a JSON")
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        for key, value in dict_json.items():
            setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        return abort(404)
