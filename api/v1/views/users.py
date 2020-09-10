#!/usr/bin/python3
"""User rule module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Get a list with all users"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get user with a specific id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user with a specific id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Create and returns the new user with the status code 201"""
    data = request.get_json()

    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)

    if "email" not in data:
        return make_response("Missing email", 400)

    if "password" not in data:
        return make_response("Missing password", 400)

    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)


if __name__ == "__main__":
    pass
