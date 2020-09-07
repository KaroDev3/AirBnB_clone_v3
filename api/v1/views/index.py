#!/usr/bin/python3
"""Index module"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def get_status():
    """Get Status"""
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    pass