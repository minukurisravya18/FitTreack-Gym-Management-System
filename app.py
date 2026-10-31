import os, logging
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from services.database import init_db
from services.members import *
from services.workouts import *
from services.analytics import summary, members_csv
from flask import Response

app=Flask(__name__); app.secret_key=os.getenv("SECRET_KEY","change-me")
logging.basicConfig(level=logging.INFO, filename="gym_system.log", format="%(asctime)s %(levelname)s %(message)s")
init_db()

@app.get("/")
def home(): return render_template("index.html", stats=summary(), members=list_members())
@app.get("/members")
def members_page(): return render_template("members.html", members=list_members(request.args.get("q","")), q=request.args.get("q",""))
@app.post("/members")
def member_form():
    try: create_member(request.form); flash("Member registered successfully.","success")
    except ValueError as e: flash(str(e),"error")
    return redirect("/members")
@app.post("/members/<int:i>/renew")
def renew_form(i):
    try: renew(i,request.form.get("plan","Monthly")); flash("Membership renewed.","success")
    except ValueError as e: flash(str(e),"error")
    return redirect("/members")
@app.get("/attendance")
def attendance_page(): return render_template("attendance.html",members=list_members(),records=attendance_history())
@app.post("/attendance")
def attendance_form():
    try: mark_attendance(request.form.get("member_id")); flash("Attendance saved.","success")
    except ValueError as e: flash(str(e),"error")
    return redirect("/attendance")
@app.get("/workouts")
def workouts_page(): return render_template("workouts.html",members=list_members(),workouts=list_workouts())
@app.post("/workouts")
def workout_form():
    try: assign_workout(request.form); flash("Workout assigned.","success")
    except ValueError as e: flash(str(e),"error")
    return redirect("/workouts")
@app.post("/workouts/<int:i>/complete")
def complete_form(i):
    try: complete_workout(i); flash("Workout completed.","success")
    except ValueError as e: flash(str(e),"error")
    return redirect("/workouts")
@app.get("/analytics")
def analytics_page(): return render_template("analytics.html",stats=summary())

@app.get("/api/health")
def health(): return jsonify(status="ok",service="Gym Management API")
@app.get("/api/members")
def api_members(): return jsonify(members=list_members(request.args.get("q","")))
@app.post("/api/members")
def api_create():
    try: return jsonify(member=create_member(request.get_json(silent=True) or {})),201
    except ValueError as e: return jsonify(error=str(e)),400
@app.get("/api/members/<int:i>")
def api_get(i):
    m=get_member(i); return (jsonify(member=m),200) if m else (jsonify(error="Member not found"),404)
@app.put("/api/members/<int:i>")
def api_update_member(i):
    try: return jsonify(member=update_member(i,request.get_json(silent=True) or {}))
    except ValueError as e: return jsonify(error=str(e)),400
@app.post("/api/members/<int:i>/renew")
def api_renew(i):
    try: return jsonify(member=renew(i,(request.get_json(silent=True) or {}).get("plan","Monthly")))
    except ValueError as e: return jsonify(error=str(e)),400
@app.get("/api/attendance")
def api_attendance(): return jsonify(attendance=attendance_history())
@app.post("/api/attendance")
def api_mark():
    try: return jsonify(attendance=mark_attendance((request.get_json(silent=True) or {}).get("member_id"))),201
    except ValueError as e: return jsonify(error=str(e)),400
@app.get("/api/workouts")
def api_workouts(): return jsonify(workouts=list_workouts(request.args.get("member_id")))
@app.post("/api/workouts")
def api_workout_create():
    try: return jsonify(workout=assign_workout(request.get_json(silent=True) or {})),201
    except ValueError as e: return jsonify(error=str(e)),400
@app.post("/api/workouts/<int:i>/complete")
def api_workout_complete(i):
    try: return jsonify(workout=complete_workout(i))
    except ValueError as e: return jsonify(error=str(e)),400
@app.get("/api/analytics")
def api_stats(): return jsonify(summary())
@app.get("/api/analytics/export.csv")
def api_csv(): return Response(members_csv(),mimetype="text/csv",headers={"Content-Disposition":"attachment; filename=members.csv"})
if __name__=="__main__": app.run(debug=os.getenv("FLASK_DEBUG","true").lower()=="true")
