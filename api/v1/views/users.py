#!/usr/bin/python3
"""
create a new view for User objects that
handles all default RESTFul API actions

"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage, user


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ lists all users """
    list_users = []
    for user in storage.all('User').values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ list a specific user through its id """
    user = storage.get('User', user_id)
    if not user:
        return make_response(jsonify({'error': "Not found"}), 404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user in the list """
    user = storage.get('User', user_id)
    if not user:
        return make_response(jsonify({'error': "Not found"}), 404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ creates a user in the users object """
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    data = request.get_json()
    if 'email' not in data:
        return make_response(jsonify({'error': "Missing email"}), 400)
    if 'password' not in data:
        return make_response(jsonify({'error': "Missing password"}), 400)
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ updates a user in the users class """
    user = storage.get('User', user_id)
    if not user:
        return make_response(jsonify({'error': "Not found"}), 404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    data = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
