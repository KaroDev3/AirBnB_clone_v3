#!/usr/bin/python3
"""Index module"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def get_status():
    """Get Status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """ retrieves the number of each objects by type """
    result = {}
    for key, value in classes.items():
        result[key] = storage.count(value)
    return jsonify(result)


if __name__ == "__main__":
    pass
