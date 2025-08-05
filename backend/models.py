from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()


class QualityLevel(Enum):
    POOR = "poor"
    QUESTIONABLE = "questionable"
    GOOD = "good"
    EXCELLENT = "excellent"


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    region = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    climate_data = db.relationship("ClimateData", backref="location", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "region": self.region,
        }


class Metric(db.Model):
    __tablename__ = "metrics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    climate_data = db.relationship("ClimateData", backref="metric", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "unit": self.unit,
            "description": self.description,
        }


class ClimateData(db.Model):
    __tablename__ = "climate_data"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    metric_id = db.Column(db.Integer, db.ForeignKey("metrics.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Numeric(10, 4), nullable=False)
    quality = db.Column(db.Enum(QualityLevel), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index("idx_location_metric_date", "location_id", "metric_id", "date"),
        db.Index("idx_date_quality", "date", "quality"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "location_id": self.location_id,
            "location_name": self.location.name,
            "latitude": float(self.location.latitude),
            "longitude": float(self.location.longitude),
            "date": self.date.strftime("%Y-%m-%d"),
            "metric": self.metric.name,
            "value": float(self.value),
            "unit": self.metric.unit,
            "quality": self.quality.value,
        }


QUALITY_WEIGHTS = {
    QualityLevel.EXCELLENT: 1.0,
    QualityLevel.GOOD: 0.8,
    QualityLevel.QUESTIONABLE: 0.5,
    QualityLevel.POOR: 0.3,
}
