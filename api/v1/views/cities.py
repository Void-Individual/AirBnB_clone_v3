#!/usr/bin/python3
"""Module to handle the city objects"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models import storage

