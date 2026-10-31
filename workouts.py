from services.database import conn
from services.members import get_member
def list_workouts(member_id=None):
    with conn() as c:
        if member_id: rows=c.execute("SELECT w.*,m.name member_name FROM workouts w JOIN members m ON m.id=w.member_id WHERE member_id=? ORDER BY w.id DESC",(member_id,)).fetchall()
        else: rows=c.execute("SELECT w.*,m.name member_name FROM workouts w JOIN members m ON m.id=w.member_id ORDER BY w.id DESC").fetchall()
    return [dict(r) for r in rows]
def assign_workout(x):
    try: mid=int(x.get("member_id")); sets=int(x.get("sets")); reps=int(x.get("repetitions")); duration=int(x.get("duration_minutes"))
    except (ValueError,TypeError): raise ValueError("Member, sets, repetitions and duration are required.")
    if not get_member(mid): raise ValueError("Member not found.")
    exercise=str(x.get("exercise_name","")).strip()
    if not exercise: raise ValueError("Exercise name is required.")
    if min(sets,reps,duration)<1: raise ValueError("Sets, repetitions and duration must be positive.")
    with conn() as c:
        cur=c.execute("INSERT INTO workouts(member_id,exercise_name,sets,repetitions,duration_minutes,trainer_notes) VALUES(?,?,?,?,?,?)",(mid,exercise,sets,reps,duration,str(x.get("trainer_notes","")).strip())); i=cur.lastrowid
    return next(w for w in list_workouts() if w["id"]==i)
def complete_workout(i):
    with conn() as c:
        if not c.execute("SELECT id FROM workouts WHERE id=?",(i,)).fetchone(): raise ValueError("Workout not found.")
        c.execute("UPDATE workouts SET status='Completed' WHERE id=?",(i,))
    return next(w for w in list_workouts() if w["id"]==i)
