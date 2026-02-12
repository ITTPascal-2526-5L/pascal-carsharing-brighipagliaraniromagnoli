from flask import Blueprint, jsonify
from app.api.cars_api import get_car_models


api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/models/<make>")
def get_models(make):
    try:
        models = get_car_models(make)
        return jsonify(models)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
