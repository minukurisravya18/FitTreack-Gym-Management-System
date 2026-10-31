# Postman API Testing
Start app with `python app.py`; base URL is `http://127.0.0.1:5000`.
Set Body > raw > JSON and Content-Type `application/json` for POST/PUT.
- GET `/api/health`
- POST `/api/members` JSON: `{"name":"Ananya","age":22,"gender":"Female","weight":60,"fitness_goal":"Strength","phone":"9876543210","plan":"Monthly"}`
- GET `/api/members`
- GET `/api/members/1`
- PUT `/api/members/1` JSON: `{"weight":59,"fitness_goal":"Fitness"}`
- POST `/api/members/1/renew` JSON: `{"plan":"Quarterly"}`
- POST `/api/attendance` JSON: `{"member_id":1}`
- GET `/api/attendance`
- POST `/api/workouts` JSON: `{"member_id":1,"exercise_name":"Squats","sets":3,"repetitions":12,"duration_minutes":20,"trainer_notes":"Keep back straight"}`
- GET `/api/workouts`
- POST `/api/workouts/1/complete`
- GET `/api/analytics`
- GET `/api/analytics/export.csv`
Invalid member data should return 400; missing member should return 404.
