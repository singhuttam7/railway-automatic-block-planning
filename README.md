# 🚆 RailOptiX

## AI-Powered Automatic Block Planning & Optimization for Indian Railways

RailOptiX is an AI-powered railway maintenance block planning and optimization system designed to coordinate maintenance activities across Engineering, Traction Distribution (TRD), and Signal & Telecommunication (S&T) departments.

The system combines an AI-based maintenance priority engine with constraint-based optimization using Google OR-Tools to generate efficient weekly and monthly block plans while considering maintenance urgency, corridor availability, train operations, and multi-department coordination.

---

## 🎯 Problem Statement

Railway maintenance activities are often planned independently by different departments. Maintenance requests, defects, asset information, corridor availability, and train schedules may exist across different systems.

This can lead to:

- Inefficient utilization of maintenance blocks
- Conflicts between maintenance activities
- Poor coordination between departments
- Increased asset downtime
- Under-utilized maintenance windows
- Unnecessary impact on train operations
- Difficulty in creating optimized weekly and monthly block plans

RailOptiX addresses these challenges through centralized data processing, AI-assisted prioritization, and mathematical optimization.

---

## 💡 Our Solution

RailOptiX integrates railway maintenance and operational information into a unified planning workflow.

The system:

1. Collects maintenance tasks, defects, assets, corridors, train schedules, and goods-train forecasts.
2. Calculates maintenance priority using criticality, urgency, and asset impact.
3. Identifies compatible maintenance activities.
4. Uses Google OR-Tools to optimize block allocation.
5. Coordinates activities across multiple departments.
6. Generates optimized block plans.
7. Provides operational impact analysis.
8. Allows planners to perform What-If simulations.
9. Presents planning insights through an interactive dashboard.

---

## ✨ Key Features

### 🤖 AI Maintenance Priority Engine

Automatically evaluates maintenance tasks and classifies them based on priority:

- Critical
- High
- Medium
- Low

Priority is influenced by factors such as:

- Asset criticality
- Maintenance urgency
- Defect severity
- Impact on asset availability

---

### 🧠 Constraint-Based Block Optimization

RailOptiX uses Google OR-Tools to determine feasible and efficient maintenance block schedules.

The optimizer considers:

- Block duration
- Corridor availability
- Maintenance requirements
- Department requirements
- Scheduling conflicts
- Train operations
- Multi-department coordination

---

### 🚧 Multi-Department Block Coordination

RailOptiX can identify maintenance activities from different departments that can potentially be performed within a coordinated block.

For example:

```text
Engineering
      +
S&T
      +
TRD
      ↓
Common Maintenance Block
```

## 🏗️ System Architecture

RailOptiX follows a modular architecture that separates data processing, maintenance prioritization, optimization, and visualization.

### Architecture Flow

```text
Railway Data
     │
     ▼
Data Integration & Processing
     │
     ▼
AI Priority Engine
     │
     ▼
Priority Classification
     │
     ▼
OR-Tools Optimization Engine
     │
     ▼
Constraint Validation
     │
     ▼
Optimized Block Plan
     │
     ├──────────────► Dashboard
     │
     ├──────────────► What-If Simulator
     │
     └──────────────► AI Intelligence
```

## 🤖 AI Maintenance Priority Engine

The RailOptiX AI Priority Engine evaluates maintenance activities and assigns a priority level based on the operational importance and urgency of each task.

The priority engine helps maintenance planners identify which activities should receive attention first before the optimization engine generates the final block schedule.

### Priority Factors

The engine considers maintenance-related factors such as:

- Asset criticality
- Maintenance urgency
- Defect severity
- Impact on asset availability

### Priority Flow

```text
Maintenance Task
       │
       ▼
Asset & Maintenance Information
       │
       ▼
Criticality Analysis
       │
       ▼
Urgency Analysis
       │
       ▼
Defect / Asset Impact Analysis
       │
       ▼
Priority Calculation
       │
       ▼
Priority Classification
       │
       ├── Critical
       ├── High
       ├── Medium
       └── Low
```

## 🧠 OR-Tools Block Optimization Engine

After maintenance activities are prioritized, RailOptiX uses Google OR-Tools to generate an optimized block plan.

The optimization engine converts prioritized maintenance requirements into feasible maintenance blocks while considering operational and scheduling constraints.

### Optimization Objective

The optimizer aims to:

- Efficiently utilize available maintenance blocks
- Reduce unnecessary infrastructure downtime
- Coordinate maintenance activities across departments
- Avoid scheduling conflicts
- Respect corridor availability
- Consider railway operational constraints
- Improve overall block utilization

### Optimization Workflow

```text
Prioritized Maintenance Tasks
            │
            ▼
     Candidate Blocks
            │
            ▼
     Constraint Analysis
            │
     ┌──────┼────────┐
     │      │        │
     ▼      ▼        ▼
 Corridor  Duration  Train
 Availability         Operations
     │      │        │
     └──────┼────────┘
            │
            ▼
   Multi-Department
      Coordination
            │
            ▼
      OR-Tools Solver
            │
            ▼
    Feasible Solutions
            │
            ▼
   Optimized Block Plan
```

## 🔌 API Documentation

RailOptiX uses a RESTful FastAPI backend to provide maintenance, planning, optimization, and operational data to the React frontend.

### API Architecture

```text
React Frontend
      │
      │ HTTP / HTTPS
      ▼
FastAPI Backend
      │
      ├── Priority Engine
      ├── Optimization Engine
      ├── Planning Services
      └── Database Services
              │
              ▼
        PostgreSQL
```

## 🐳 Docker Deployment

RailOptiX is fully containerized for consistent development and production deployment.

The application uses separate containers for the frontend and backend, while PostgreSQL provides persistent database storage.

### Docker Architecture

```text
                    Docker / Render
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
┌────────────────────┐       ┌────────────────────┐
│ Frontend Container │       │ Backend Container  │
│                    │       │                    │
│ React + Vite       │       │ FastAPI            │
│ Nginx              │       │ Python             │
│ Port 80            │       │ Port 8000          │
└─────────┬──────────┘       └─────────┬──────────┘
          │                            │
          │ HTTP/HTTPS                 │
          └──────────────┬─────────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ PostgreSQL       │
                │ Database         │
                └──────────────────┘
```

## 🔐 Environment Variables & Security

RailOptiX uses environment variables to separate application configuration from source code.

### Backend Environment Variables

Create:

```text
backend/.env
```

## ☁️ Production Deployment

RailOptiX is deployed using Docker-based services on Render with PostgreSQL as the production database.

### Production Architecture

```text
                         GitHub
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
     Frontend Service           Backend Service
              │                         │
       Docker + Nginx            Docker + FastAPI
              │                         │
              │ HTTPS                │
              └────────────┬──────────┘
                           │
                           ▼
                  Render PostgreSQL
```

## 📊 Optimization Results

RailOptiX was tested using the synthetic railway maintenance dataset and generated an optimized planning schedule.

### AI Priority Engine Results

The priority engine processed:

- **450 maintenance tasks**
- **9 Critical**
- **37 High**
- **81 Medium**
- **323 Low**

Priority is determined using factors such as:

- Asset criticality
- Maintenance urgency
- Defect severity
- Impact on asset availability

### Block Optimization Results

The OR-Tools optimization engine generated:

| Metric                     | Result |
| -------------------------- | -----: |
| Total Optimized Blocks     |    105 |
| Planning Days              |     29 |
| Total Block Hours          |  242.5 |
| Multi-Department Blocks    |     20 |
| Average Optimization Score |  49.95 |

### Multi-Department Coordination

The optimizer identified opportunities to consolidate maintenance activities from multiple departments into coordinated blocks.

For example:

```text
Engineering ─┐
             ├──► Coordinated Maintenance Block
S&T ─────────┤
             │
TRD ─────────┘
```

## 🚀 Future Scope

RailOptiX is designed as a scalable foundation for intelligent railway maintenance block planning. The current prototype can be extended with the following capabilities.

### 1. Real Railway Data Integration

Integrate RailOptiX with real railway information systems such as:

- TMS — Track Management System
- SMMS — Signal Maintenance Management System
- TDMS — Traction Distribution Management System
- BDMS — Block Demand Management System
- COA — Control Office Application

This would enable automated collection of maintenance requirements, defects, corridor availability and operational constraints.

### 2. Real-Time Train Operations

Integrate live train movement and timetable information to dynamically adjust maintenance blocks according to current railway operations.

### 3. Dynamic Block Re-Optimization

When unexpected events occur, such as:

- Train delays
- Emergency maintenance
- New critical defects
- Corridor unavailability
- Weather-related disruptions

the optimization engine could automatically recalculate the affected blocks.

### 4. Advanced Machine Learning

Future versions can use historical railway maintenance data to improve:

- Maintenance priority prediction
- Failure probability estimation
- Maintenance duration prediction
- Asset degradation prediction
- Operational impact prediction

### 5. Digital Twin

A railway corridor digital twin could be developed to simulate infrastructure, maintenance activities and train operations before executing a block plan.

### 6. Explainable AI

The system can provide detailed explanations for:

- Why a task received a particular priority
- Why a maintenance block was selected
- Why tasks were consolidated
- Why a particular scheduling alternative was rejected

This can improve transparency and support operational decision-making.

### 7. Natural Language Railway Assistant

An optional AI assistant could allow planners to ask questions such as:

> "Show me all critical maintenance tasks for next week."

> "Which blocks can be consolidated between Engineering and S&T?"

> "What happens if this corridor becomes unavailable?"

The assistant would interact with the existing planning and optimization services rather than replacing the optimization engine.

### 8. Mobile Support

A responsive mobile application could provide field engineers and railway officials with:

- Assigned maintenance blocks
- Block status
- Task details
- Alerts
- Corridor information
- Real-time updates

### 9. Role-Based Access Control

Future production deployments can introduce role-based permissions for:

- Control Office
- Engineering
- Signal & Telecommunication
- Traction Distribution
- Maintenance Supervisors
- Administrators

### 10. Enterprise-Scale Deployment

The system can be extended with:

- Distributed services
- Background optimization jobs
- Redis/Celery task processing
- Monitoring and logging
- Automated backups
- High-availability PostgreSQL
- Kubernetes-based deployment

These improvements would help transition RailOptiX from a prototype into a production-grade railway planning platform.
