#!/usr/bin/python3
"""Module to contain the index file with an implemented blueprint
"""

from models.amenity import Amenity
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.review import Review
from models import storage
from models.state import State
from models.user import User


classes = {"amenity": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """Default status function"""
    return {"status": "OK"}


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Function to show the stats of all classes"""
    
    stats = {}
    for cls in classes.keys():
        count = storage.count(classes[cls])
        stats[cls] = count
    return stats
