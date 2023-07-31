#!/usr/bin/python3
"""
create a new view for Place objects that
handles all default RESTFul API actions

"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage, place, city, user


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """ lists all places of a city """
    city = storage.get('City', city_id)
    if not city:
        return make_response(jsonify({'error': "Not found"}), 404)
    list_places = [place.to_dict() for place in city.places]
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ list a specific place through its id """
    place = storage.get('Place', place_id)
    if not place:
        return make_response(jsonify({'error': "Not found"}), 404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place in the list """
    place = storage.get('Place', place_id)
    if not place:
        return make_response(jsonify({'error': "Not found"}), 404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ creates a place in the places object """
    city = storage.get('City', city_id)
    if not city:
        return make_response(jsonify({'error': "Not found"}), 404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    data = request.get_json()
    if 'user_id' not in data:
        return make_response(jsonify({'error': "Missing user_id"}), 400)
    user = storage.get('User', data['user_id'])
    if not user:
        return make_response(jsonify({'error': "Not found"}), 404)
    if 'name' not in data:
        return make_response(jsonify({'error': "Missing name"}), 400)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ updates a place in the places class """
    place = storage.get('Place', place_id)
    if not place:
        return make_response(jsonify({'error': "Not found"}), 404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
