
# Railway Automatic Block Planning

An AI-powered automatic block planning system for Indian Railways that integrates maintenance, defect, corridor, and train operation data to generate optimized maintenance block schedules.

## Problem Statement

Railway maintenance activities for Engineering, Traction Distribution (TRD), and Signal & Telecommunication (S&T) departments are currently planned independently. This decentralized approach can result in inefficient block utilization, poor coordination between departments, increased asset downtime, and disruption to train operations.

## Proposed Solution

The system aims to provide a centralized, data-driven platform that:

* Integrates maintenance and defect data from TMS, SMMS, and TDMS
* Integrates train timetable, corridor availability, and goods-train forecasts
* Prioritizes maintenance activities based on criticality, urgency, safety risk, and asset impact
* Coordinates maintenance activities across multiple departments
* Optimizes maintenance block schedules using operational constraints
* Generates weekly and monthly maintenance plans
* Provides explainable recommendations and what-if scheduling simulations
* Maximizes asset availability while minimizing downtime and train disruption

## System Architecture

```text
TMS ─────┐
SMMS ────┤
TDMS ────┤
COA ─────┤──► Data Integration
BDMS ────┘          │
                    ▼
             AI Priority Engine
                    │
                    ▼
           Block Optimization Engine
                    │
                    ▼
          Weekly / Monthly Block Plan
                    │
                    ▼
             Web Dashboard
```

## Key Features

* Multi-department maintenance coordination
* AI-based maintenance priority scoring
* Automatic block scheduling
* Train conflict detection
* Corridor availability analysis
* Multi-department block consolidation
* Weekly and monthly planning
* Asset availability monitoring
* What-if simulation
* Explainable AI recommendations
* Planning and performance reports

## Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL

### AI/ML

* Python
* Pandas
* NumPy
* Scikit-learn

### Optimization

* Google OR-Tools

### Frontend

* React
* Tailwind CSS
* Recharts

## Project Status

🚧 **Under Development**

### Development Roadmap

* [x] Project initialization
* [x] Backend environment setup
* [ ] Synthetic railway dataset
* [ ] Database design
* [ ] FastAPI backend
* [ ] Maintenance priority engine
* [ ] Block optimization engine
* [ ] Weekly planning
* [ ] Monthly planning
* [ ] React dashboard
* [ ] What-if simulator
* [ ] Reports and analytics
* [ ] Testing
* [ ] Dockerization
* [ ] Deployment

## Disclaimer

This project is a prototype developed for demonstration and research purposes. Railway systems and operational data are represented using simulated/synthetic data unless otherwise specified.
