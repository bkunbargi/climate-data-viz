from flask import Blueprint, jsonify

metrics_bp = Blueprint("metrics", __name__)


@metrics_bp.route("/api/v1/metrics", methods=["GET"])
def get_metrics():
    """
    Retrieve all available climate metrics.
    """
    try:
        from models import Metric

        metrics = Metric.query.all()
        return jsonify({"data": [metric.to_dict() for metric in metrics]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
