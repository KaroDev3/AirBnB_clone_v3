#!/usr/bin/python3
"""Places Reviews rule module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User

@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """Get a list with all reviews of a place"""
    reviews = []
    is_valid_id = False
    for place in storage.all(Place).values():
        if place.id == place_id:
            is_valid_id = True
            break
    if not is_valid_id:
        abort(404)
    for review in storage.all(Review).values():
        if review.place_id == place_id:
            reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Get a review with a specific id"""
    for review in storage.all(Review).values():
        if review.id == review_id:
            return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a review with a specific id"""
    for review in storage.all(Review).values():
        if review.id == review_id:
            storage.delete(review)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Create and returns the new review with the status code 201"""
    # check if 'place_id' is a valid ID
    is_valid_id = False
    for place in storage.all(Place).values():
        if place.id == place_id:
            is_valid_id = True
            break
    if not is_valid_id:
        abort(404)

    # check if data is JSON and has key 'user_id'
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)
    if "user_id" not in data:
        return make_response("Missing user_id", 400)

    # check if 'user_id' is a valid ID
    is_valid_id = False
    for user in storage.all(User).values():
        if user.id == data['user_id']:
            is_valid_id = True
            break
    if not is_valid_id:
        abort(404)

    # check if data has key 'text'
    if "text" not in data:
        return make_response("Missing text", 400)

    # creates the new review
    data['place_id'] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Updates a Review object"""
    target_review = None
    for review in storage.all(Review).values():
        if review.id == review_id:
            target_review = review
    if target_review is None:
        abort(404)
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'created_at']:
            setattr(target_city, key, value)
    storage.save()
    return make_response(jsonify(target_review.to_dict()), 200)


if __name__ == "__main__":
    pass
