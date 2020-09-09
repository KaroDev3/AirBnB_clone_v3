#!/usr/bin/python3
"""State rule module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Get a list with all places"""
    places = []
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            places.append(place.to_dict())
    if places == []:
        abort(404)
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get a place with a specific id"""
    for place in storage.all(Place).values():
        if place.id == place_id:
            return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a place with a specific id"""
    for place in storage.all(Place).values():
        if place.id == place_id:
            storage.delete(place)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Create and returns the new place with the status code 201"""
    is_valid_id = False
    for city in storage.all(City).values():
        if city.id == city_id:
            is_valid_id = True
            break

    if not is_valid_id:
        abort(404)

    is_valid_id = False
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)

    if "user_id" not in data:
        return make_response("Missing user_id", 400)

    for user in storage.all(User).values():
        if user.id == data["user_id"]:
            is_valid_id = True
            break

    if not is_valid_id:
        abort(404)

    if "name" not in data:
        return make_response("Missing name", 400)

    data["city_id"] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    target_place = None
    for place in storage.all(Place).values():
        if place.id == place_id:
            target_place = place
    if target_place is None:
        abort(404)
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(target_place, key, value)
    storage.save()
    return make_response(jsonify(target_place.to_dict()), 200)


if __name__ == "__main__":
    pass
