from flask import Blueprint, jsonify, request
from datetime import datetime

climate_bp = Blueprint("climate", __name__)


@climate_bp.route("/api/v1/climate", methods=["GET"])
def get_climate_data():
    """
    Retrieve climate data with optional filtering.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold
    """
    try:
        from models import ClimateData, Location, Metric, QualityLevel

        location_id = request.args.get("location_id", type=int)
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        metric = request.args.get("metric")
        quality_threshold = request.args.get("quality_threshold")
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 50, type=int), 100)

        query = ClimateData.query.join(Location).join(Metric)

        if location_id:
            query = query.filter(ClimateData.location_id == location_id)

        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
                query = query.filter(ClimateData.date >= start_date_obj)
            except ValueError:
                return (
                    jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}),
                    400,
                )

        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
                query = query.filter(ClimateData.date <= end_date_obj)
            except ValueError:
                return (
                    jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}),
                    400,
                )

        if metric:
            query = query.filter(Metric.name == metric)

        if quality_threshold:
            quality_levels = {
                "poor": [
                    QualityLevel.POOR,
                    QualityLevel.QUESTIONABLE,
                    QualityLevel.GOOD,
                    QualityLevel.EXCELLENT,
                ],
                "questionable": [
                    QualityLevel.QUESTIONABLE,
                    QualityLevel.GOOD,
                    QualityLevel.EXCELLENT,
                ],
                "good": [QualityLevel.GOOD, QualityLevel.EXCELLENT],
                "excellent": [QualityLevel.EXCELLENT],
            }

            if quality_threshold not in quality_levels:
                return (
                    jsonify(
                        {
                            "error": "Invalid quality_threshold. Use: poor, questionable, good, excellent"
                        }
                    ),
                    400,
                )

            query = query.filter(
                ClimateData.quality.in_(quality_levels[quality_threshold])
            )

        total_count = query.count()

        climate_data = query.order_by(ClimateData.date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify(
            {
                "data": [data.to_dict() for data in climate_data.items],
                "meta": {
                    "total_count": total_count,
                    "page": page,
                    "per_page": per_page,
                },
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
