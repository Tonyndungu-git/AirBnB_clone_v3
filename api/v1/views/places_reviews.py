#!/usr/bin/python3
"""
create a new view for Review objects that
handles all default RESTFul API actions

"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage, review, place, user


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """ lists all reviews of a place """
    place = storage.get('Place', place_id)
    if not place:
        return make_response(jsonify({'error': "Not found"}), 404)
    list_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ list a specific review through its id """
    review = storage.get('Review', review_id)
    if not review:
        return make_response(jsonify({'error': "Not found"}), 404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review in the list """
    review = storage.get('Review', review_id)
    if not review:
        return make_response(jsonify({'error': "Not found"}), 404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """ creates a review in the reviews object """
    place = storage.get('Place', place_id)
    if not place:
        return make_response(jsonify({'error': "Not found"}), 404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    data = request.get_json()
    if 'user_id' not in data:
        return make_response(jsonify({'error': "Missing user_id"}), 400)
    user = storage.get('User', data['user_id'])
    if not user:
        return make_response(jsonify({'error': "Not found"}), 404)
    if 'text' not in data:
        return make_response(jsonify({'error': "Missing text"}), 400)
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ updates a review in the reviews class """
    review = storage.get('Review', review_id)
    if not review:
        return make_response(jsonify({'error': "Not found"}), 404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
