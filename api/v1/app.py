#!/usr/bin/python3
"""API module v1"""

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown(self):
    """Removes the current SQLAlchemy Session"""
    from models import storage
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Response on Error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', '5000')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
