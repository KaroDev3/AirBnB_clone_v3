#!/usr/bin/python3
"""View for the link between Place objects and Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from models import *


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_all_amenities_of_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    # check if the Place with ID 'place_id' exists
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # retrieves Amenities depending of the storage
    if storage_t == "db":
        # list Amenity objects from amenities relationship
        amenities = []
        for amenity in place.amenities:
            amenities.append(amenity.to_dict())
        return jsonify(amenities)
    else:
        # list Amenity ID in the list amenity_ids
        return jsonify(place.amenity_ids)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_of_place(place_id, amenity_id):
    """Deletes a Amenity of a Place"""
    # check if the Place with ID 'place_id' exists
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # check if the Amenity with ID 'amenity_id' exists
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    # Delete the 'amenity' of 'place'
    # raise 404 error if 'amenity' is not linked
    # using index because .pop() deletes an index
    for i in range(len(place.amenities)):
        if place.amenities[i].id == amenity.id:
            place.amenities.pop(i)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenity_to_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    # check if the Place with ID 'place_id' exists
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # check if the Amenity with ID 'amenity_id' exists
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    # ckeck if Amenity is already linked to Place
    for place_amenity in place.amenities:
        if amenity.id == place_amenity.id:
            return make_response(jsonify(amenity.to_dict()), 200)

    # link the Amenity to a Place
    place.amenities.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
