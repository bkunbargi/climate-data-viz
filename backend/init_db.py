#!/usr/bin/env python3
"""
Database initialization script for EcoVision Climate Visualizer
This script creates the database, tables, and seeds initial data from sample_data.json
"""

import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Location, Metric, ClimateData, QualityLevel

load_dotenv()


def load_sample_data():
    """Load sample data from JSON file"""
    data_file = os.path.join(
        os.path.dirname(__file__), "..", "data", "sample_data.json"
    )
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find sample data file at {data_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in sample data file: {e}")
        sys.exit(1)


def seed_locations(locations_data):
    """Seed locations table"""
    for location_data in locations_data:
        existing = Location.query.filter_by(id=location_data["id"]).first()
        if existing:
            print(f"  Location {location_data['name']} already exists, skipping...")
            continue

        location = Location(
            id=location_data["id"],
            name=location_data["name"],
            country=location_data["country"],
            latitude=location_data["latitude"],
            longitude=location_data["longitude"],
            region=location_data.get("region"),
        )
        db.session.add(location)
        print(f"  Added location: {location.name}")

    db.session.commit()
    print(f"✓ Seeded {len(locations_data)} locations")


def seed_metrics(metrics_data):
    """Seed metrics table"""
    print("Seeding metrics...")
    for metric_data in metrics_data:
        existing = Metric.query.filter_by(id=metric_data["id"]).first()
        if existing:
            print(f"  Metric {metric_data['name']} already exists, skipping...")
            continue

        metric = Metric(
            id=metric_data["id"],
            name=metric_data["name"],
            display_name=metric_data["display_name"],
            unit=metric_data["unit"],
            description=metric_data["description"],
        )
        db.session.add(metric)
        print(f"  Added metric: {metric.display_name}")

    db.session.commit()
    print(f"✓ Seeded {len(metrics_data)} metrics")


def seed_climate_data(climate_data):
    """Seed climate data table"""
    print("Seeding climate data...")
    added_count = 0

    for data_point in climate_data:
        existing = ClimateData.query.filter_by(id=data_point["id"]).first()
        if existing:
            continue

        quality_map = {
            "poor": QualityLevel.POOR,
            "questionable": QualityLevel.QUESTIONABLE,
            "good": QualityLevel.GOOD,
            "excellent": QualityLevel.EXCELLENT,
        }

        quality = quality_map.get(data_point["quality"])
        if not quality:
            print(
                f"  Warning: Invalid quality level '{data_point['quality']}' for data point {data_point['id']}"
            )
            continue

        try:
            date = datetime.strptime(data_point["date"], "%Y-%m-%d").date()
        except ValueError as e:
            print(
                f"  Warning: Invalid date format '{data_point['date']}' for data point {data_point['id']}: {e}"
            )
            continue

        climate_reading = ClimateData(
            id=data_point["id"],
            location_id=data_point["location_id"],
            metric_id=data_point["metric_id"],
            date=date,
            value=data_point["value"],
            quality=quality,
        )
        db.session.add(climate_reading)
        added_count += 1

    db.session.commit()
    print(f"✓ Seeded {added_count} climate data points")


def init_database():
    """Initialize the database with tables and sample data"""
    print("=== EcoVision Database Initialization ===")

    app = create_app()

    with app.app_context():

        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created")

        print("Loading sample data...")
        sample_data = load_sample_data()

        seed_locations(sample_data["locations"])
        seed_metrics(sample_data["metrics"])
        seed_climate_data(sample_data["climate_data"])

        print("\n=== Database initialization complete! ===")
        print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")

        location_count = Location.query.count()
        metric_count = Metric.query.count()
        climate_data_count = ClimateData.query.count()

        print(f"\nData Summary:")
        print(f"  Locations: {location_count}")
        print(f"  Metrics: {metric_count}")
        print(f"  Climate Data Points: {climate_data_count}")


def test_connection():
    """Test database connection"""
    print("Testing database connection...")
    app = create_app()

    with app.app_context():
        try:

            location_count = Location.query.count()
            print(
                f"✓ Database connection successful! Found {location_count} locations."
            )
            return True
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
            return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_connection()
    else:
        init_database()
