# Gym Management & Fitness Analytics System
Flask + SQLite + Pandas + NumPy + Chart.js internship project.

## Features
- Member registration/profile fields: name, age, gender, weight, goal, phone, join date, membership status
- Monthly/Quarterly/Yearly plans and renewal tracking
- Daily attendance, duplicate attendance prevention
- Workout assignment, sets, reps, duration, trainer notes, completion tracking
- Analytics for active/expired members, monthly registrations, attendance trends, popular workouts, plan distribution, illustrative revenue
- REST API, CSV export, validation, logging, SQLite persistence

## Run on Windows
1. Extract ZIP and open folder in VS Code.
2. Open Terminal:
   `python -m venv .venv`
   `.venv\\Scripts\\activate`
   `pip install -r requirements.txt`
   `python app.py`
3. Visit `http://127.0.0.1:5000`. Keep terminal open while using the app.

## Pages
`/` dashboard, `/members`, `/attendance`, `/workouts`, `/analytics`.

## API
See `docs/API_TESTING.md`. Main endpoints: `/api/health`, `/api/members`, `/api/members/<id>`, `/api/attendance`, `/api/workouts`, `/api/analytics`, `/api/analytics/export.csv`.

## Notes
Revenue is an illustrative estimate; change the plan prices in `services/analytics.py` for actual gym rates. This starter does not include authentication; add access controls before using real private data or deploying publicly. Set `FLASK_DEBUG=false` in production.
