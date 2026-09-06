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
