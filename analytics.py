import io
from datetime import date
import pandas as pd, numpy as np
from services.database import conn
def summary():
    today=date.today().isoformat(); month=date.today().replace(day=1).isoformat()
    with conn() as c:
        m=pd.read_sql_query("SELECT * FROM members",c); a=pd.read_sql_query("SELECT * FROM attendance",c); w=pd.read_sql_query("SELECT * FROM workouts",c)
    active=int(((m.expiry_date>=today)&(m.membership_status=="Active")).sum()) if len(m) else 0
    expired=int((m.expiry_date<today).sum()) if len(m) else 0
    new=int((m.join_date>=month).sum()) if len(m) else 0
    trends=[{"date":str(k),"count":int(v)} for k,v in a.groupby("attendance_date").size().sort_index().items()] if len(a) else []
    popular=[{"exercise":str(k),"assignments":int(v)} for k,v in w.groupby("exercise_name").size().sort_values(ascending=False).items()] if len(w) else []
    plans=[{"plan":str(k),"members":int(v)} for k,v in m.groupby("plan").size().items()] if len(m) else []
    prices={"Monthly":1000,"Quarterly":2700,"Yearly":10000}
    revenue=int(np.sum([prices.get(p,0) for p in m.plan])) if len(m) else 0
    return {"total_members":int(len(m)),"active_members":active,"expired_memberships":expired,"monthly_new_registrations":new,"today_attendance":int((a.attendance_date==today).sum()) if len(a) else 0,"attendance_trends":trends,"popular_workouts":popular,"membership_distribution":plans,"estimated_membership_revenue":revenue,"revenue_note":"Illustrative plan prices; edit prices in services/analytics.py."}
def members_csv():
    with conn() as c: df=pd.read_sql_query("SELECT * FROM members",c)
    out=io.StringIO(); df.to_csv(out,index=False); return out.getvalue()
