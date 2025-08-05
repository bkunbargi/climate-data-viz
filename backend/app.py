from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


load_dotenv()


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    CORS(app)

    mysql_host = os.environ.get("MYSQL_HOST", "localhost")
    mysql_user = os.environ.get("MYSQL_USER", "root")
    mysql_password = os.environ.get("MYSQL_PASSWORD", "")
    mysql_db = os.environ.get("MYSQL_DB", "climate_data")

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        if mysql_password:
            database_url = (
                f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
            )
        else:
            database_url = "sqlite:///climate_data.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    from models import db

    db.init_app(app)

    migrate = Migrate(app, db)

    from routes.climate import climate_bp
    from routes.locations import locations_bp
    from routes.metrics import metrics_bp
    from routes.summary import summary_bp
    from routes.trends import trends_bp

    app.register_blueprint(climate_bp)
    app.register_blueprint(locations_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(summary_bp)
    app.register_blueprint(trends_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
