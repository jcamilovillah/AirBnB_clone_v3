#!/usr/bin/python3
"""RestFul API actions User
"""
from models.user import User
from models import storage
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieves all users
    """
    users = storage.all(User).values()
    list_users = []
    for user in users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def one_user(user_id=None):
    """Retrieve an user
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id=None):
    """Delete user object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """Create an user
    """
    dict_json = request.get_json()
    if not dict_json:
        abort(400, description="Not a JSON")
    if 'email' not in dict_json:
        abort(400, description="Missing email")
    if 'password' not in dict_json:
        abort(400, description="Missing password")

    new_user = User(**dict_json)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id=None):
    """Update an user
    """
    dict_json = request.get_json()
    ignore = ['id', 'email', 'created_at', 'updated_at']
    if not dict_json:
        abort(400, description="Not a JSON")
    user = storage.get(User, user_id)
    if user:
        for key, value in dict_json.items():
            if key not in ignore:
                setattr(user, key, value)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
    else:
        return abort(404)
