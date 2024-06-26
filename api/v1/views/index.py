#!/usr/bin/python3
"""Module to contain the index file with an implemented blueprint
"""
from flask import jsonify
from models.amenity import Amenity
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.review import Review
from models import storage
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Default status function"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Function to show the stats of all classes"""

    stats = {}
    for cls in classes.keys():
        count = storage.count(classes[cls])
        stats[cls] = count
    return jsonify(stats)
