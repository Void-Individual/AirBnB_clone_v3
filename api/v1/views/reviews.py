#!/usr/bin/python3
"""Module for the review objects"""

from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_of_place(place_id):
    """Function to retrieve the reviews of a place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = storage.all(Review).values()
    place_reviews = []
    for review in reviews:
        if review.place_id == place_id:
            place_reviews.append(review.to_dict())
    return jsonify(place_reviews)


@app_views.route('/reviews/<id>', methods=['GET'], strict_slashes=False)
def get_review(id):
    """Function to retrieve a review with id"""

    review = storage.get(Review, id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<id>', methods=['DELETE'], strict_slashes=False)
def delete_review(id):
    """Function to delete a review"""

    review = storage.get(Review, id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Function to create a new review"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<id>', methods=['PUT'], strict_slashes=False)
def update_review(id):
    """Function to update the details of a review"""

    review = storage.get(Review, id)
    if review is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
