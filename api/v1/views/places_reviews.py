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
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Get a review with a specific id"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a review with a specific id"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Create and returns the new review with the status code 201"""
    # check if 'place_id' is a valid ID
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    # check if data is JSON and has key 'user_id'
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)
    if "user_id" not in data:
        return make_response("Missing user_id", 400)

    # check if 'user_id' is a valid ID
    user = storage.get(User, data['user_id'])

    if user is None:
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
    # check if the Review with ID 'review_id' exists
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    # check if data is a JSON
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)

    # updates the Review
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()
    return make_response(jsonify(review.to_dict()), 200)


if __name__ == "__main__":
    pass
