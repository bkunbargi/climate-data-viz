# EcoVision: Climate Data Visualizer

A full-stack web application for visualizing and analyzing climate data with interactive dashboards, trend analysis, and data quality indicators.

## What It Does

EcoVision provides climate data visualization through:

• Interactive charts for temperature, precipitation, and humidity data
• Filtering by location, date range, metric type, and data quality
• Trend analysis with pattern detection and anomaly identification
• Data quality indicators and reliability scoring
• Responsive web interface

## Architecture

### Backend (Flask API)
• RESTful API with 5 endpoints for climate data, locations, metrics, summaries, and trends
• Quality-weighted statistical calculations
• SQLite database with migration support
• Filtering and pagination for datasets

### Frontend (React Dashboard)
• Charts using Chart.js for data visualization
• Real-time filtering and data updates
• Multiple view modes: raw data, summaries, and trend analysis
• Quality indicators for data reliability

## Tech Stack

**Backend:**
• Flask + SQLAlchemy + Flask-Migrate
• SQLite database (configurable for MySQL)
• Python 3.8+

**Frontend:**
• React 18 + Vite
• Chart.js for visualizations
• TailwindCSS for styling
• Node.js 16+

## Quick Start

### 1. Backend Setup
```bash
cd backend
# See backend/README.md for detailed setup instructions
```

### 2. Frontend Setup  
```bash
cd frontend
# See frontend/README.md for detailed setup instructions
```

## Setup Instructions

Each component has its own setup guide:

• [Backend Setup](backend/README.md) - API server, database, and migration instructions
• [Frontend Setup](frontend/README.md) - React dashboard and development server

Both support automated and manual setup options.

## Sample Data

• 3 locations: Irvine, Tokyo, London
• 3 climate metrics: Temperature (°C), Precipitation (mm), Humidity (%)
• Quality levels: Excellent → Good → Questionable → Poor
• 40 sample data points with quality variations

## API Endpoints

• `GET /api/v1/locations` - Available locations
• `GET /api/v1/metrics` - Climate metrics
• `GET /api/v1/climate` - Climate data with filtering
• `GET /api/v1/summary` - Statistical summaries
• `GET /api/v1/trends` - Trend analysis with anomaly detection

## Development

• Database migrations for schema changes
• Quality weighting for statistical calculations
• Error handling with proper HTTP status codes
• Responsive design

## Access

Once running:
• Backend API: http://localhost:5000
• Frontend Dashboard: http://localhost:3000 