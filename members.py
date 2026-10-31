from datetime import date,timedelta
from services.database import conn
PLANS={"Monthly":30,"Quarterly":90,"Yearly":365}
def d(r): return dict(r) if r else None
def list_members(q=""):
    with conn() as c:
        rows=c.execute("SELECT * FROM members WHERE name LIKE ? OR phone LIKE ? ORDER BY id DESC",(f"%{q}%",f"%{q}%")).fetchall()
    return [dict(x) for x in rows]
def get_member(i):
    with conn() as c: return d(c.execute("SELECT * FROM members WHERE id=?",(i,)).fetchone())
def create_member(x):
    name=str(x.get("name","")).strip()
    if not name: raise ValueError("Member name is required.")
    plan=str(x.get("plan","Monthly")).title()
    if plan not in PLANS: raise ValueError("Choose Monthly, Quarterly or Yearly.")
    try: age=int(x["age"]) if x.get("age") not in (None,"") else None; weight=float(x["weight"]) if x.get("weight") not in (None,"") else None
    except (ValueError,TypeError): raise ValueError("Age and weight must be numbers.")
    if age is not None and not 1<=age<=120: raise ValueError("Age must be 1-120.")
    if weight is not None and not 1<=weight<=500: raise ValueError("Weight must be 1-500 kg.")
    today=date.today()
    with conn() as c:
        cur=c.execute("INSERT INTO members(name,age,gender,weight,fitness_goal,phone,plan,join_date,membership_status,expiry_date) VALUES(?,?,?,?,?,?,?,?,?,?)",(name,age,x.get("gender") or None,weight,str(x.get("fitness_goal","")).strip(),str(x.get("phone","")).strip(),plan,today.isoformat(),"Active",(today+timedelta(days=PLANS[plan])).isoformat()))
        i=cur.lastrowid
    return get_member(i)
def update_member(i,x):
    m=get_member(i)
    if not m: raise ValueError("Member not found.")
    allowed={"name","age","gender","weight","fitness_goal","phone","plan"}
    for k,v in x.items():
        if k not in allowed: continue
        if k=="name" and not str(v).strip(): raise ValueError("Name cannot be empty.")
        if k=="plan" and str(v).title() not in PLANS: raise ValueError("Invalid membership plan.")
        with conn() as c: c.execute(f"UPDATE members SET {k}=? WHERE id=?",(v,i))
    return get_member(i)
def renew(i,plan):
    plan=str(plan).title()
    if plan not in PLANS: raise ValueError("Choose Monthly, Quarterly or Yearly.")
    m=get_member(i)
    if not m: raise ValueError("Member not found.")
    start=max(date.today(),date.fromisoformat(m["expiry_date"]))
    with conn() as c: c.execute("UPDATE members SET plan=?,membership_status='Active',expiry_date=? WHERE id=?",(plan,(start+timedelta(days=PLANS[plan])).isoformat(),i))
    return get_member(i)
def mark_attendance(i):
    try: i=int(i)
    except (ValueError,TypeError): raise ValueError("Select a member.")
    m=get_member(i)
    if not m: raise ValueError("Member not found.")
    if m["expiry_date"]<date.today().isoformat(): raise ValueError("Membership expired; renew first.")
    with conn() as c:
        c.execute("INSERT OR IGNORE INTO attendance(member_id,attendance_date) VALUES(?,?)",(i,date.today().isoformat()))
        r=c.execute("SELECT * FROM attendance WHERE member_id=? AND attendance_date=?",(i,date.today().isoformat())).fetchone()
    return dict(r)
def attendance_history():
    with conn() as c: rows=c.execute("SELECT a.*,m.name member_name FROM attendance a JOIN members m ON m.id=a.member_id ORDER BY attendance_date DESC").fetchall()
    return [dict(r) for r in rows]
