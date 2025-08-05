# Climate Data API

## Requirements
• Python 3.8+ (use `python` or `python3` based on your system)

## Setup

### Option 1: Automated
• `python -m venv venv`
• `source venv/bin/activate`
• `python setup.py` (sets up everything: dependencies, database, migration tracking)

### Option 2: Manual
• `python -m venv venv`
• `source venv/bin/activate`
• `pip install -r requirements.txt`
• `python init_db.py`
• `python migrate_db.py init`

## Run
• `python app.py`
• API runs at http://localhost:5000

## Database Management

### When You Change Models
• `python migrate_db.py create "describe your change"`
• `python migrate_db.py apply`

### Migration Tools
• `python migrate_db.py history` (view all migrations)
• `python migrate_db.py current` (current database version)
• `python migrate_db.py downgrade base` (reset to empty database)

### Quick Reset
• `rm instance/climate_data.db && python init_db.py` (fresh start)

### Test
• `python init_db.py test` (should show 3 locations)
