#!/usr/bin/env python3
"""
Database migration helper script for EcoVision Climate Visualizer
Provides easy commands for managing database schema changes
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv()


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"{description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        if result.stdout:
            print(result.stdout)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False


def init_migrations():
    """Initialize migrations directory (first time setup)"""
    if os.path.exists("migrations"):
        print("✓ Migrations directory already exists")
        return True

    return run_command("flask db init", "Initializing migrations")


def create_migration(message=None):
    """Create a new migration file"""
    if not message:
        message = input("Enter migration description: ").strip()
        if not message:
            message = "Auto-generated migration"

    command = f'flask db migrate -m "{message}"'
    return run_command(command, f"Creating migration: {message}")


def apply_migrations():
    """Apply pending migrations to database"""
    return run_command("flask db upgrade", "Applying migrations")


def show_migration_history():
    """Show migration history"""
    return run_command("flask db history", "Migration history")


def show_current_revision():
    """Show current database revision"""
    return run_command("flask db current", "Current database revision")


def downgrade_migration(revision=None):
    """Downgrade to a specific revision"""
    if not revision:
        revision = input(
            "Enter revision to downgrade to (or 'base' for clean slate): "
        ).strip()
        if not revision:
            print("No revision specified, cancelling")
            return False

    command = f"flask db downgrade {revision}"
    return run_command(command, f"Downgrading to revision: {revision}")


def main():
    """Main migration management interface"""
    print("=== EcoVision Database Migration Manager ===")

    if len(sys.argv) < 2:
        print(
            """
Usage: python migrate_db.py <command> [options]

Commands:
  init                    Initialize migrations (first time setup)
  create [message]        Create a new migration
  apply                   Apply pending migrations  
  history                 Show migration history
  current                 Show current database revision
  downgrade [revision]    Downgrade to specific revision
  
Examples:
  python migrate_db.py init
  python migrate_db.py create "Add user table"
  python migrate_db.py apply
  python migrate_db.py downgrade base
"""
        )
        return

    command = sys.argv[1].lower()

    if command == "init":
        init_migrations()

    elif command == "create":
        message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        if not os.path.exists("migrations"):
            print("Migrations not initialized. Running init first...")
            if init_migrations():
                create_migration(message)
        else:
            create_migration(message)

    elif command == "apply":
        apply_migrations()

    elif command == "history":
        show_migration_history()

    elif command == "current":
        show_current_revision()

    elif command == "downgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else None
        downgrade_migration(revision)

    else:
        print(f"Unknown command: {command}")
        print("Run 'python migrate_db.py' for help")


if __name__ == "__main__":
    main()
