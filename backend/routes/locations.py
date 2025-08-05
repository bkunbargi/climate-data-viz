from flask import Blueprint, jsonify

locations_bp = Blueprint("locations", __name__)


@locations_bp.route("/api/v1/locations", methods=["GET"])
def get_locations():
    """
    Retrieve all available locations.
    """
    try:
        from models import Location

        locations = Location.query.all()
        return jsonify({"data": [location.to_dict() for location in locations]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
