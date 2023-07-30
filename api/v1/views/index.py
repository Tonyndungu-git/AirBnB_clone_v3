""" api/v1/views/index.py """
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """ returns json response """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """
    Retrieves the number of each object by type
    """
    classes = {
        'Amenity': 'amenities',
        'City': 'cities',
        'Place': 'places',
        'Review': 'reviews',
        'State': 'states',
        'User': 'users'
    }

    stats = {class_name: storage.count(class_name) for class_name in classes}

    return jsonify(stats)
