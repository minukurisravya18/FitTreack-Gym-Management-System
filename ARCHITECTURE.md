# Architecture
Browser or Postman -> Flask routes (`app.py`) -> service modules (`services/`) -> SQLite (`gym.db`). Analytics service processes records with Pandas and NumPy and serves JSON/CSV; Chart.js renders dashboard charts.
Tables: members (profile/membership), attendance (one row per member/date), workouts (exercise plan and completion status).
