#!/usr/bin/env python3
"""
Setup script for EcoVision Climate Visualizer backend
"""

import os
import sys
import subprocess


def install_requirements():
    """Install Python requirements"""
    print("Installing Python requirements...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False


def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("✓ .env file already exists")
        return True

    example_file = "env_example.txt"
    if os.path.exists(example_file):
        print("Creating .env file from example...")
        with open(example_file, "r") as f:
            content = f.read()

        with open(env_file, "w") as f:
            f.write(content)

        print("✓ .env file created")
        print("Please edit .env file with your database credentials")
        return True
    else:
        print("No env_example.txt found, creating basic .env file")
        basic_env = """# Database Configuration (SQLite fallback)
DATABASE_URL=sqlite:///climate_data.db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
"""
        with open(env_file, "w") as f:
            f.write(basic_env)
        print("✓ Basic .env file created with SQLite")
        return True


def main():
    """Main setup function"""
    print("=== EcoVision Backend Setup ===")

    # Check if we're in a virtual environment
    if not hasattr(sys, "real_prefix") and not (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("Warning: You might not be in a virtual environment")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != "y":
            print(
                "Setup cancelled. Please activate your virtual environment and try again."
            )
            sys.exit(1)

    if not install_requirements():
        sys.exit(1)

    create_env_file()

    print("\nInitializing database...")
    try:
        from init_db import init_database

        init_database()
        print("✓ Database initialization complete")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        print(
            "You can try running 'python init_db.py' manually after configuring your database"
        )

    print("\nSetting up migration tracking...")
    try:
        result = subprocess.run(
            [sys.executable, "migrate_db.py", "init"], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print("✓ Migration tracking setup complete")
        else:
            print("✓ Migration tracking already initialized")
    except Exception as e:
        print(f"Migration tracking setup failed: {e}")
        print("You can run 'python migrate_db.py init' manually later")

    print("\n=== Setup Complete! ===")
    print("Next steps:")
    print("1. Edit .env file with your database credentials (if using MySQL)")
    print("2. Run 'python app.py' to start the development server")
    print("3. Test the API at http://localhost:5000/api/v1/locations")


if __name__ == "__main__":
    main()
