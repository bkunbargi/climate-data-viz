from flask import Blueprint, jsonify, request
from datetime import datetime
import statistics

trends_bp = Blueprint("trends", __name__)


@trends_bp.route("/api/v1/trends", methods=["GET"])
def get_trends():
    """
    Analyze trends and patterns in climate data.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold
    """
    try:
        from models import ClimateData, Location, Metric, QualityLevel

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

        data = query.order_by(ClimateData.date.asc()).all()

        trends_summary = {}
        by_metric = {}
        for item in data:
            metric_name = item.metric.name
            if metric_name not in by_metric:
                by_metric[metric_name] = []
            by_metric[metric_name].append(item)

        for metric_name, metric_data in by_metric.items():
            if len(metric_data) < 2:
                continue

            values = [float(item.value) for item in metric_data]
            dates = [item.date for item in metric_data]

            mid_point = len(values) // 2
            first_half_avg = sum(values[:mid_point]) / mid_point if mid_point > 0 else 0
            second_half_avg = sum(values[mid_point:]) / (len(values) - mid_point)

            if second_half_avg > first_half_avg * 1.05:
                direction = "increasing"
                rate = round((second_half_avg - first_half_avg) / len(values), 4)
            elif second_half_avg < first_half_avg * 0.95:
                direction = "decreasing"
                rate = round((first_half_avg - second_half_avg) / len(values), 4)
            else:
                direction = "stable"
                rate = 0

            high_quality_count = sum(
                1 for item in metric_data if item.quality.value in ["excellent", "good"]
            )
            confidence = min(0.95, 0.4 + (high_quality_count / len(metric_data)) * 0.5)

            anomalies = []
            if len(values) > 3:
                mean_val = statistics.mean(values)
                stdev_val = statistics.stdev(values)

                for item in metric_data:
                    value = float(item.value)
                    deviation = abs(value - mean_val)
                    if deviation > 2 * stdev_val:
                        anomalies.append(
                            {
                                "date": item.date.strftime("%Y-%m-%d"),
                                "value": round(value, 2),
                                "deviation": round(deviation / stdev_val, 1),
                                "quality": item.quality.value,
                                "location": item.location.name,
                                "location_id": item.location_id,
                                "coordinates": {
                                    "latitude": float(item.location.latitude),
                                    "longitude": float(item.location.longitude),
                                },
                            }
                        )

            seasonality = {
                "detected": len(values) > 8,
                "period": "monthly" if len(values) > 8 else "insufficient_data",
                "confidence": 0.6 if len(values) > 8 else 0.1,
            }

            unit = metric_data[0].metric.unit

            trends_summary[metric_name] = {
                "trend": {
                    "direction": direction,
                    "rate": rate,
                    "unit": f"{unit}/period",
                    "confidence": round(confidence, 2),
                },
                "anomalies": anomalies[:5],
                "seasonality": seasonality,
            }

        return jsonify({"data": trends_summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
