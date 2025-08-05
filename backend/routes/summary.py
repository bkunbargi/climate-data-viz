from flask import Blueprint, jsonify, request
from datetime import datetime

summary_bp = Blueprint("summary", __name__)


@summary_bp.route("/api/v1/summary", methods=["GET"])
def get_summary():
    """
    Retrieve quality-weighted summary statistics for climate data.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold
    """
    try:
        from models import ClimateData, Location, Metric, QualityLevel, QUALITY_WEIGHTS

        location_id = request.args.get("location_id", type=int)
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        metric_filter = request.args.get("metric")
        quality_threshold = request.args.get("quality_threshold")

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

        if metric_filter:
            query = query.filter(Metric.name == metric_filter)

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
                return jsonify({"error": "Invalid quality_threshold"}), 400

            query = query.filter(
                ClimateData.quality.in_(quality_levels[quality_threshold])
            )

        data = query.all()

        metrics_summary = {}

        by_metric = {}
        for item in data:
            metric_name = item.metric.name
            if metric_name not in by_metric:
                by_metric[metric_name] = []
            by_metric[metric_name].append(item)

        for metric_name, metric_data in by_metric.items():
            if not metric_data:
                continue

            values = [float(item.value) for item in metric_data]
            weights = [QUALITY_WEIGHTS[item.quality] for item in metric_data]

            min_val = min(values)
            max_val = max(values)
            avg_val = sum(values) / len(values)

            weighted_sum = sum(v * w for v, w in zip(values, weights))
            weight_sum = sum(weights)
            weighted_avg = weighted_sum / weight_sum if weight_sum > 0 else 0

            quality_counts = {}
            for item in metric_data:
                quality = item.quality.value
                quality_counts[quality] = quality_counts.get(quality, 0) + 1

            total_count = len(metric_data)
            quality_distribution = {
                quality: count / total_count
                for quality, count in quality_counts.items()
            }

            unit = metric_data[0].metric.unit

            metrics_summary[metric_name] = {
                "min": round(min_val, 2),
                "max": round(max_val, 2),
                "avg": round(avg_val, 2),
                "weighted_avg": round(weighted_avg, 2),
                "unit": unit,
                "quality_distribution": quality_distribution,
            }

        return jsonify({"data": metrics_summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
