# IIACC Survey Analysis & Program Evaluation

A data analysis project supporting the Indiana Infant and Toddler Community Connections (IIACC) program. This pipeline ingests multi-year survey data, cleans and reconciles it, and generates interactive visualizations and exportable summaries to surface participation trends and program gaps.

---

## Overview

This project was built to help program stakeholders answer questions like:
- How has participation changed year over year?
- Where are gaps in outreach by region or demographic?
- How satisfied are members with meetings, communication formats, and facilitation?

The analysis spans participation, feedback, role demographics, regional engagement, and communication channel ratings — all broken down by survey year.

---

## What's in the Code

### Data Loading & Cleaning
- Reads a CSV survey export and coerces `Event Name` (survey year) to numeric
- Filters out incomplete/placeholder entries (e.g., year 2025)
- Splits data into per-year dictionaries for grouped analysis


### Column Groups Analyzed
- **Participation**: news, Google, CAG, IIACC, interviews, focus groups
- **Feedback**: workgroup, large group, meeting format/length/topics, facilitation, activities
- **News/Comms Feedback**: newsletter format, frequency, content; Google Group layout/usability
- **Roles**: primary role, medical role, other roles, role term
- **Demographics**: gender, ethnicity, residence, area description
- **Regional Work**: NW, NE, NC, C, E, SE, SW, outside Indiana

---

## Tech Stack


Python (pandas) - Data cleaning, grouping, aggregation 
Matplotlib - Bar charts, line charts, interactive navigation 
Seaborn - Heatmaps 
NumPy - Axis tick generation
Excel - (PivotTables, VLOOKUP) Data reconciliation and gap checks 
Tableau - KPI dashboards — engagement rates, participation trends, survey completion 
SQL - Ad hoc analysis for outreach efficacy evaluation 
REDCap - Longitudinal data collection instrument management 

---

## How to Run

1. Clone the repo and install dependencies:
```bash
pip install pandas matplotlib seaborn numpy
```

2. Update the file path in the script:
```python
file_path = r"path/to/your/survey_data.csv"
```

3. Run the script:
```bash
python iiacc_analysis.py
```

The interactive chart window will open first. Use the **Next** button to cycle through all plots. Additional static charts (stacked bars, heatmap, line chart) will follow sequentially.

---

## Key Insights Enabled

- Identified **participation gaps by region and channel** to guide targeted outreach
- Tracked **year-over-year feedback trends** on meeting quality and communication formats
- Surfaced **demographic and role patterns** among IIACC members to support equity-focused programming
- Delivered findings via Tableau dashboards and summary reports to cross-functional stakeholder teams

---

## Project Context

This analysis was developed as part of program evaluation work supporting a public health initiative focused on early childhood community coordination across Indiana. Data collection instruments were managed in REDCap; cleaned outputs fed into Tableau dashboards monitored in real time by program leadership.
