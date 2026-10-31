import os, sqlite3
DB=os.getenv("GYM_DB_PATH","gym.db")
def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; c.execute("PRAGMA foreign_keys=ON"); return c
def init_db():
    with conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,age INTEGER,gender TEXT,weight REAL,fitness_goal TEXT,phone TEXT,plan TEXT NOT NULL DEFAULT 'Monthly',join_date TEXT NOT NULL DEFAULT(date('now')),membership_status TEXT NOT NULL DEFAULT 'Active',expiry_date TEXT NOT NULL DEFAULT(date('now','+30 days')));
        CREATE TABLE IF NOT EXISTS attendance(id INTEGER PRIMARY KEY AUTOINCREMENT,member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,attendance_date TEXT NOT NULL DEFAULT(date('now')),UNIQUE(member_id,attendance_date));
        CREATE TABLE IF NOT EXISTS workouts(id INTEGER PRIMARY KEY AUTOINCREMENT,member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,exercise_name TEXT NOT NULL,sets INTEGER NOT NULL,repetitions INTEGER NOT NULL,duration_minutes INTEGER NOT NULL,trainer_notes TEXT,status TEXT NOT NULL DEFAULT 'Assigned',assigned_date TEXT NOT NULL DEFAULT(date('now')));
        """)
