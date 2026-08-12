# Athlete KPI Tracker & Risk Assessment

A desktop app for coaches to log athlete training data and flag injury risk before it becomes an injury. Built around the **Acute:Chronic Workload Ratio (ACWR)**, a sports-science metric that compares an athlete's recent (7-day) training load against their longer-term (28-day) baseline to catch dangerous spikes in workload.

<!-- TODO: add a screenshot or GIF of the Coach Dashboard here -->
![Coach Dashboard screenshot placeholder](docs/coach-dashboard.png)

<!-- TODO: add a GIF of the Add Athlete -> Check-In -> Dashboard flow here -->
![App walkthrough GIF placeholder](docs/walkthrough.gif)

## Why this exists

Coaches and PTs track training volume by feel more often than by data due to not having the resources that college/professional coaches have. ACWR gives an accessible evidence-based signal: when an athlete's short-term load spikes well above their chronic baseline, injury risk rises sharply. This app turns that signal into something a coach can actually see and act on, day to day.

## Features

- **Add Athlete** — onboard a new athlete with name, sport, and coach/PT email.
- **Athlete Check-In** — log a daily training entry (duration, RPE, sleep, soreness) with input validation.
- **Coach Dashboard** — a live table of every athlete's latest entry, ACWR, and risk status, color coded and with specific alert messages (e.g. "ACWR spike to 1.62").
- **Risk engine** — computes rolling acute/chronic workload and flags:
  - ACWR > 1.5 → `RED` (critical spike)
  - ACWR > 1.3 → `YELLOW` (elevated)
  - Low sleep (< 6.5 hrs) + high soreness (≥ 4) → `YELLOW`
- Seeded sample data on first run so the dashboard is populated immediately with one athlete per status.

## Tech stack

- **Python** with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the desktop UI
- **SQLModel** (SQLAlchemy + Pydantic) over **SQLite** for persistence
- **pandas** for the rolling window ACWR calculation
- **pytest** for testing

## Getting started

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

On first run the app creates `tracker.db` and seeds four sample athletes (printed to the console with their IDs) so the Coach Dashboard isn't empty.

## Running tests

```bash
pytest
```

Covers the risk calculation edge cases (insufficient data, steady baseline, workload spike, sleep/soreness combo), the alert email formatting logic, database models, and seeding.

## Project structure

```
main.py                    # app entry point, tab layout
database/
  models.py                 # Athlete, DailyLog (SQLModel)
  db_engine.py               # SQLite engine/session setup
  seed.py                    # sample data seeding
analytics/
  risk_calc.py                # ACWR calculation + dashboard row assembly
notifications/
  alert_service.py            # SMTP email alerts (send_alert_email)
ui/
  add_athlete_view.py          # Add Athlete tab
  athlete_view.py               # Athlete Check-In tab
  coach_view.py                  # Coach Dashboard tab
tests/                         # pytest tests
```

## Roadmap

This is an actively evolving project. Some of the following improvements being worked on:

- **Alert emails aren't connected yet.** `notifications/alert_service.py` has a working, tested `send_alert_email()` and each `Athlete` has `coach_email`/`pt_email` fields, but nothing calls it yet — a `RED`/`YELLOW` status currently just shows in the dashboard table rather than notifying anyone. Connecting this to the risk check is next.
- **No CI pipeline** running the test suite on push.
- **Create-only logs** — no edit/delete for daily log entries yet.
