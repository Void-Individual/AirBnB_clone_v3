#!/usr/bin/python3
"""Module to control all other files for the flask
application"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close(exception):
    """Close the db on teardown"""

    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Render a custom 404 JSON"""

    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
