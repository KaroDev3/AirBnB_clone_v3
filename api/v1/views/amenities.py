#!/usr/bin/python3
"""Amenity rule module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Get a list with all amenities"""
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Get an amenity with a specific id"""
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity with a specific id"""
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def post_amenity():
    """Create and returns the new amenity with the status code 201"""
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)
    if "name" not in data:
        return make_response("Missing name", 400)
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Updates an Amenity object"""
    target_amenity = None
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            target_amenity = amenity
    if target_amenity is None:
        abort(404)
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(target_amenity, key, value)
    storage.save()
    return make_response(jsonify(target_amenity.to_dict()), 200)


if __name__ == "__main__":
    pass
