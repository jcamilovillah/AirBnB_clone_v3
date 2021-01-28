#!/usr/bin/python3
"""Show index"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """return status"""
    return jsonify({"status": "OK"})
