from flask import Flask, request, redirect, url_for, session, render_template_string, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "AquaShield_AI_2026"

INCIDENTS = [
    {"id":1,"location":"MG Road Junction","water":46,"department":"Traffic Department","status":"Road Restricted","risk":"HIGH","description":"Heavy water accumulation. Traffic should be avoided.","officer":"Amit Sharma","reported":"11:10 AM"},
    {"id":2,"location":"Railway Underpass","water":22,"department":"Municipal Department","status":"Under Review","risk":"MEDIUM","description":"Waterlogging detected near the underpass.","officer":"Neha Verma","reported":"10:55 AM"},
    {"id":3,"location":"Bus Stand Road","water":8,"department":"Road Department","status":"Resolved","risk":"LOW","description":"Minor water accumulation.","officer":"Rohan Patel","reported":"10:20 AM"},
    {"id":4,"location":"Civil Hospital Road","water":52,"department":"Disaster Management","status":"Officer Assigned","risk":"HIGH","description":"Heavy flooding reported. Emergency access required.","officer":"Priya Singh","reported":"11:25 AM"}
]

OFFICERS = [
    {"id":1,"name":"Amit Sharma","department":"Traffic","area":"MG Road","status":"Active"},
    {"id":2,"name":"Neha Verma","department":"Municipal","area":"Railway Zone","status":"Active"},
    {"id":3,"name":"Rohan Patel","department":"Road Department","area":"Bus Stand","status":"Available"},
    {"id":4,"name":"Priya Singh","department":"Disaster Management","area":"Civil Hospital","status":"Active"}
]

WARNINGS = [
    {"location":"MG Road Junction","risk":"HIGH","message":"Avoid MG Road Junction because of dangerous flooding.","status":"Published"},
    {"location":"Civil Hospital Road","risk":"HIGH","message":"Avoid unnecessary travel on Civil Hospital Road.","status":"Published"}
]

SETTINGS = {"high":35,"medium":15,"authority":"AquaShield Authority Control Room"}

def logged_in():
    return session.get("admin") is True

def calculate_risk(water):
    if water >= SETTINGS["high"]: return "HIGH"
    if water >= SETTINGS["medium"]: return "MEDIUM"
    return "LOW"

def next_id():
    return max([i["id"] for i in INCIDENTS], default=0) + 1

def get_incident(iid):
    return next((i for i in INCIDENTS if i["id"] == iid), None)
@app.route("/api/incidents", methods=["POST"])
def receive_incident():
    data = request.get_json(silent=True) or {}

    location = data.get("location", "Unknown Location")
    water = int(data.get("water", 0))
    department = data.get("department", "Emergency Control")
    status = data.get("status", "New Incident")
    source = data.get("source", "GIS / AI")

    incident = {
        "id": next_id(),
        "location": location,
        "water": water,
        "department": department,
        "status": status,
        "risk": calculate_risk(water),
        "source": source
    }

    INCIDENTS.append(incident)

    return {
        "success": True,
        "message": "Incident received successfully",
        "incident": incident
    }, 201


CSS = r"""
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI",Arial,sans-serif;background:#eef5fa;color:#17324d;font-size:15px}
a,a:hover,a:visited,a:active{text-decoration:none!important}
.sidebar{position:fixed;left:0;top:0;bottom:0;width:250px;background:linear-gradient(180deg,#031b3d,#063b76,#02182f);color:white;padding:22px 15px;overflow-y:auto}
.logo{display:flex;align-items:center;gap:12px;margin-bottom:30px;padding:5px;color:white}
.logo-icon{width:48px;height:48px;border-radius:14px;background:linear-gradient(135deg,#10c9e5,#0879ed);display:flex;align-items:center;justify-content:center;font-size:26px}
.logo b{font-size:17px}.logo small{display:block;font-size:10px;color:#a9cce1;margin-top:3px}
.nav-title{color:#7fa2c1;font-size:10px;font-weight:bold;margin:22px 10px 9px;letter-spacing:1px}
.nav{display:block;padding:13px 12px;margin:5px 0;border-radius:10px;color:#d1e1ec;font-size:14px;font-weight:600;transition:.2s}
.nav:hover,.nav.active{background:#0878e5;color:white}
.main{margin-left:250px}
.topbar{height:68px;background:#052755;color:white;display:flex;align-items:center;justify-content:space-between;padding:0 28px;font-size:13px}
.online{color:#c9ead8}.green-dot{display:inline-block;width:9px;height:9px;background:#20d56b;border-radius:50%;margin-right:6px}
.content{padding:28px;max-width:1550px;margin:auto}
.flash{background:#e7f7ed;border:1px solid #c7ead5;color:#126c3d;padding:14px;border-radius:10px;margin-bottom:18px;font-size:14px}
.heading{display:flex;justify-content:space-between;align-items:center;gap:15px;margin-bottom:20px}
.heading h1{margin:0;font-size:30px;font-weight:800}.heading p{margin:7px 0;color:#71869a;font-size:14px}
.btn{display:inline-block;border:0;border-radius:9px;padding:12px 17px;background:linear-gradient(135deg,#087be3,#08a5c3);color:white!important;font-weight:700;font-size:13px;cursor:pointer;transition:.2s;text-decoration:none!important}
.btn:hover{transform:translateY(-1px);opacity:.92}.btn.red{background:#df3945}.btn.green{background:#149c59}.btn.gray{background:#eaf1f6;color:#34536b!important}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px}
.card{background:white;border:1px solid #e5edf3;border-radius:14px;padding:20px;box-shadow:0 6px 20px rgba(10,50,80,.06)}
.card-title{color:#71869a;font-size:11px;font-weight:800;letter-spacing:.5px}.number{font-size:34px;font-weight:800;margin:8px 0}.card-small{color:#8ca0af;font-size:12px}
.brief{margin:18px 0;padding:20px;border-radius:14px;background:linear-gradient(110deg,#05244b,#096995);color:white}
.brief h3{margin:0;font-size:17px}.brief p{font-size:13px;color:#c6e0ed;line-height:1.6}
.panel{background:white;border-radius:14px;border:1px solid #e5edf3;overflow:hidden;margin-top:18px;box-shadow:0 5px 18px rgba(10,50,80,.04)}
.panel-head{padding:17px;border-bottom:1px solid #e8eef3;display:flex;justify-content:space-between;align-items:center;gap:15px}
table{width:100%;border-collapse:collapse}th{background:#f7fafc;color:#70869a;text-align:left;padding:14px;font-size:11px;font-weight:800}
td{padding:15px 14px;border-top:1px solid #edf2f5;font-size:13px}td b{font-size:14px}
.badge{display:inline-block;padding:7px 11px;border-radius:20px;font-size:11px;font-weight:800}.high{background:#ffe6e8;color:#c52d38}.medium{background:#fff2d2;color:#966900}.low{background:#e5f7ec;color:#117444}
.action{display:flex;gap:7px;flex-wrap:wrap}
.form{padding:22px;display:grid;grid-template-columns:1fr 1fr;gap:18px}.field label{display:block;font-size:12px;font-weight:800;margin-bottom:7px;color:#5c7388}
input,select,textarea{width:100%;border:1px solid #dbe5ed;border-radius:9px;padding:13px;font-family:inherit;font-size:14px;outline:none}
input:focus,select:focus,textarea:focus{border-color:#0785df;box-shadow:0 0 0 3px rgba(8,133,223,.08)}textarea{min-height:110px}.full{grid-column:1/-1}
.warning{background:#fff4f4;border-left:5px solid #e33b45;padding:17px;border-radius:9px;margin:12px 0;font-size:13px;line-height:1.6}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.tile{background:white;padding:22px;border-radius:14px;border:1px solid #e5edf3}.tile h3{font-size:17px}.tile p{color:#70869a;font-size:13px;line-height:1.7}
.footer{margin-top:18px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.footer-box{background:#062d5a;color:white;padding:16px;border-radius:10px;font-size:11px}.footer-box b{font-size:16px}
.login-page{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:25px;background:linear-gradient(135deg,#021936,#075b88,#09a8c2)}
.login-box{width:900px;max-width:96%;display:grid;grid-template-columns:1fr 1fr;background:white;border-radius:24px;overflow:hidden;box-shadow:0 25px 70px rgba(0,0,0,.35)}
.login-left{padding:50px;color:white;background:linear-gradient(145deg,#031b3b,#075c8d,#09a5bf)}.login-left .big{font-size:52px}.login-left h1{font-size:34px;margin:18px 0}.login-left p{font-size:14px;line-height:1.8;color:#c9e3ed}.login-right{padding:50px}.login-right h2{font-size:28px}.login-right label{display:block;margin-top:18px;margin-bottom:7px;font-size:13px;font-weight:800}.login-right input{font-size:15px;padding:14px}.login-right .btn{width:100%;margin-top:20px;font-size:15px;padding:14px}
.secure{display:inline-block;background:#e8f7ee;color:#147541;padding:8px 12px;border-radius:20px;font-size:11px;font-weight:800}.demo{margin-top:18px;padding:14px;background:#f0f6fa;border-radius:9px;font-size:12px;color:#647b8e;line-height:1.7}
@media(max-width:1050px){.sidebar{width:210px}.main{margin-left:210px}.stats{grid-template-columns:1fr 1fr}.tiles{grid-template-columns:1fr 1fr}.footer{grid-template-columns:1fr 1fr}}
@media(max-width:750px){.sidebar{display:none}.main{margin-left:0}.content{padding:18px}.topbar{padding:0 15px;font-size:11px}.heading{align-items:flex-start;flex-direction:column}.heading h1{font-size:25px}.stats,.tiles{grid-template-columns:1fr 1fr}.form{grid-template-columns:1fr}.full{grid-column:auto}.footer{grid-template-columns:1fr 1fr}.panel{overflow-x:auto}table{min-width:750px}.login-box{grid-template-columns:1fr}.login-left{display:none}}
@media(max-width:480px){.stats,.tiles,.footer{grid-template-columns:1fr}.number{font-size:30px}}
"""

PAGE = """<!doctype html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{title}} - AquaShield AI</title><style>""" + CSS + """</style></head><body>
{% if logged %}
<aside class="sidebar">
<a class="logo" href="{{url_for('dashboard')}}"><div class="logo-icon">🛡️</div><div><b>AquaShield AI</b><small>Authority Control Room</small></div></a>
<a class="nav {% if page=='dashboard' %}active{% endif %}" href="{{url_for('dashboard')}}">🏠 Dashboard</a>
<div class="nav-title">OPERATIONS</div>
<a class="nav {% if page=='incidents' %}active{% endif %}" href="{{url_for('incidents')}}">🌊 Flood Incidents</a>
<a class="nav {% if page=='add' %}active{% endif %}" href="{{url_for('add_incident')}}">➕ Add Incident</a>
<a class="nav {% if page=='officers' %}active{% endif %}" href="{{url_for('officers')}}">👮 Officers</a>
<a class="nav {% if page=='warnings' %}active{% endif %}" href="{{url_for('warnings')}}">🚨 Public Warnings</a>
<a class="nav {% if page=='analytics' %}active{% endif %}" href="{{url_for('analytics')}}">📊 Analytics & Reports</a>
<div class="nav-title">SYSTEM</div>
<a class="nav {% if page=='settings' %}active{% endif %}" href="{{url_for('settings')}}">⚙️ Settings</a>
<a class="nav {% if page=='help' %}active{% endif %}" href="{{url_for('help_page')}}">❓ Help & Support</a>
<a class="nav" href="{{url_for('logout')}}">🚪 Logout</a>
</aside>
<div class="main"><div class="topbar"><span>🌧️ Monsoon Response • Live Flood Intelligence System</span><span class="online"><span class="green-dot"></span>System Online | 👤 Admin</span></div><div class="content">
{% with messages=get_flashed_messages() %}{% for message in messages %}<div class="flash">✅ {{message}}</div>{% endfor %}{% endwith %}
{{body|safe}}</div></div>
{% else %}{{body|safe}}{% endif %}
</body></html>"""

@app.route("/")
def home():
    return redirect(url_for("dashboard" if logged_in() else "login"))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form.get("username")=="admin" and request.form.get("password")=="admin123":
            session["admin"]=True
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.")
    body="""<div class="login-page"><div class="login-box"><div class="login-left"><div class="big">🛡️</div><h1>AquaShield AI</h1><p>Smart Flood Intelligence & Authority Response System.</p><p>🌊 Flood Monitoring<br>🧠 Risk Classification<br>🚨 Emergency Alerts<br>👮 Authority Response</p></div><div class="login-right"><span class="secure">🔒 SECURE ADMIN ACCESS</span><h2>Welcome Back 👋</h2><p style="color:#71869a">Sign in to access the AquaShield Authority Control Room.</p><form method="POST"><label>USERNAME</label><input name="username" placeholder="Enter admin username" required><label>PASSWORD</label><input type="password" name="password" placeholder="Enter password" required><button class="btn" type="submit">🚀 Login to Control Room</button></form><div class="demo">💡 <b>Demo Login</b><br>Username: <b>admin</b><br>Password: <b>admin123</b></div></div></div></div>"""
    return render_template_string(PAGE,title="Admin Login",logged=False,body=body)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if not logged_in(): return redirect(url_for("login"))
    total=len(INCIDENTS); high=sum(i["risk"]=="HIGH" for i in INCIDENTS); active=sum(i["status"]!="Resolved" for i in INCIDENTS); resolved=sum(i["status"]=="Resolved" for i in INCIDENTS)
    body=render_template_string("""<div class="heading"><div><h1>Flood Response, at a glance. 🌊</h1><p>A clear view of dangerous roads and the teams responding to them.</p></div><a class="btn" href="{{url_for('add_incident')}}">➕ Add Flood Incident</a></div>
<div class="stats"><div class="card"><div class="card-title">TOTAL INCIDENTS</div><div class="number">{{total}}</div><div class="card-small">🌊 All reported locations</div></div><div class="card"><div class="card-title">🔴 HIGH RISK</div><div class="number">{{high}}</div><div class="card-small">Needs authority attention</div></div><div class="card"><div class="card-title">🟡 ACTIVE RESPONSE</div><div class="number">{{active}}</div><div class="card-small">Teams currently engaged</div></div><div class="card"><div class="card-title">🟢 RESOLVED TODAY</div><div class="number">{{resolved}}</div><div class="card-small">Successfully resolved</div></div></div>
<div class="brief"><h3>🚨 Authority Briefing</h3><p>High-risk incidents require immediate attention. Coordinate with field officers and prepare public warnings to reduce exposure to flooded roads.</p></div>
<div class="panel"><div class="panel-head"><b>🌊 Dangerous Roads & Flood Alerts</b><a class="btn gray" href="{{url_for('incidents')}}">View All</a></div><table><tr><th>LOCATION</th><th>RISK</th><th>WATER LEVEL</th><th>DEPARTMENT</th><th>STATUS</th><th>ACTION</th></tr>{% for i in incidents %}<tr><td>📍 <b>{{i.location}}</b><br><span style="color:#8296a7">{{i.description}}</span></td><td><span class="badge {{i.risk.lower()}}">{{i.risk}}</span></td><td>💧 {{i.water}} cm</td><td>{{i.department}}</td><td>{{i.status}}</td><td><div class="action"><a class="btn gray" href="{{url_for('view_incident',iid=i.id)}}">View</a>{% if i.status!="Resolved" %}<a class="btn green" href="{{url_for('resolve_incident',iid=i.id)}}">✓</a>{% endif %}</div></td></tr>{% endfor %}</table></div>
<div class="footer"><div class="footer-box">🕒 Last Updated<br><b>{{time}}</b></div><div class="footer-box">📍 Monitored Zones<br><b>18 Areas</b></div><div class="footer-box">👮 Active Officers<br><b>{{officer_count}}</b></div><div class="footer-box">🚨 Quick Alert<br><b>{{high}} High Risk</b></div></div>""",incidents=INCIDENTS,total=total,high=high,active=active,resolved=resolved,time=datetime.now().strftime("%I:%M %p"),officer_count=len(OFFICERS))
    return render_template_string(PAGE,title="Dashboard",logged=True,page="dashboard",body=body)

@app.route("/incidents")
def incidents():
    if not logged_in(): return redirect(url_for("login"))
    search=request.args.get("search","").lower()
    filtered=[i for i in INCIDENTS if search in i["location"].lower() or search in i["risk"].lower() or search in i["department"].lower()]
    body=render_template_string("""<div class="heading"><div><h1>Flood Incidents 🌊</h1><p>Monitor all reported flooded roads and locations.</p></div><a class="btn" href="{{url_for('add_incident')}}">➕ Add Incident</a></div><div class="panel"><div class="panel-head"><b>All Flood Alerts</b><form><input name="search" value="{{search}}" placeholder="🔎 Search location..."></form></div><table><tr><th>LOCATION</th><th>RISK</th><th>WATER</th><th>DEPARTMENT</th><th>OFFICER</th><th>STATUS</th><th>ACTION</th></tr>{% for i in incidents %}<tr><td>📍 <b>{{i.location}}</b></td><td><span class="badge {{i.risk.lower()}}">{{i.risk}}</span></td><td>💧 {{i.water}} cm</td><td>{{i.department}}</td><td>👮 {{i.officer}}</td><td>{{i.status}}</td><td><a class="btn gray" href="{{url_for('view_incident',iid=i.id)}}">View</a></td></tr>{% else %}<tr><td colspan="7" style="text-align:center;padding:25px">No incidents found.</td></tr>{% endfor %}</table></div>""",incidents=filtered,search=search)
    return render_template_string(PAGE,title="Flood Incidents",logged=True,page="incidents",body=body)

@app.route("/add",methods=["GET","POST"])
def add_incident():
    if not logged_in(): return redirect(url_for("login"))
    if request.method=="POST":
        try: water=int(request.form.get("water",0))
        except ValueError: water=0
        INCIDENTS.append({"id":next_id(),"location":request.form.get("location","Unknown Location"),"water":water,"department":request.form.get("department","Municipal Department"),"status":"Under Review","risk":calculate_risk(water),"description":request.form.get("description","Flooding reported."),"officer":"Unassigned","reported":datetime.now().strftime("%I:%M %p")})
        flash(f"Incident added successfully. AI risk classification: {INCIDENTS[-1]['risk']}.")
        return redirect(url_for("incidents"))
    body="""<div class="heading"><div><h1>Add Flood Incident ➕</h1><p>Enter a newly reported flooded road or location.</p></div></div><div class="panel"><form method="POST"><div class="form"><div class="field"><label>LOCATION</label><input name="location" placeholder="e.g. MG Road Junction" required></div><div class="field"><label>WATER LEVEL (CM)</label><input type="number" name="water" min="0" placeholder="e.g. 42" required></div><div class="field"><label>DEPARTMENT</label><select name="department"><option>Traffic Department</option><option>Municipal Department</option><option>Road Department</option><option>Disaster Management</option></select></div><div class="field"><label>REPORT TYPE</label><select><option>Flood / Waterlogging</option><option>Road Blockage</option><option>Emergency Access Issue</option></select></div><div class="field full"><label>DESCRIPTION</label><textarea name="description" placeholder="Describe the situation..." required></textarea></div><div class="field full"><button class="btn" type="submit">🌊 Add & Analyze Incident</button></div></div></form></div>"""
    return render_template_string(PAGE,title="Add Incident",logged=True,page="add",body=body)

@app.route("/incident/<int:iid>")
def view_incident(iid):
    if not logged_in(): return redirect(url_for("login"))
    i=get_incident(iid)
    if not i: return redirect(url_for("incidents"))
    body=render_template_string("""<div class="heading"><div><h1>{{i.location}} 📍</h1><p>Incident details and response controls.</p></div><a class="btn gray" href="{{url_for('incidents')}}">← Back</a></div><div class="stats"><div class="card"><div class="card-title">RISK LEVEL</div><div class="number"><span class="badge {{i.risk.lower()}}">{{i.risk}}</span></div></div><div class="card"><div class="card-title">WATER LEVEL</div><div class="number">💧 {{i.water}} cm</div></div><div class="card"><div class="card-title">OFFICER</div><div class="number" style="font-size:20px">👮 {{i.officer}}</div></div><div class="card"><div class="card-title">STATUS</div><div class="number" style="font-size:20px">{{i.status}}</div></div></div><div class="panel"><div class="panel-head"><b>🚨 Situation Details</b></div><div style="padding:22px;font-size:14px;line-height:2.1"><b>Location:</b> {{i.location}}<br><b>Water Level:</b> {{i.water}} cm<br><b>Department:</b> {{i.department}}<br><b>Reported:</b> {{i.reported}}<br><b>Description:</b> {{i.description}}</div></div><div class="panel"><div class="panel-head"><b>⚡ Response Actions</b></div><div style="padding:18px" class="action"><a class="btn green" href="{{url_for('resolve_incident',iid=i.id)}}">✓ Mark Resolved</a><a class="btn" href="{{url_for('assign_officer',iid=i.id)}}">👮 Assign Officer</a><a class="btn red" href="{{url_for('publish_warning',iid=i.id)}}">📢 Public Warning</a></div></div>""",i=i)
    return render_template_string(PAGE,title="Incident",logged=True,page="incidents",body=body)

@app.route("/resolve/<int:iid>")
def resolve_incident(iid):
    if not logged_in(): return redirect(url_for("login"))
    i=get_incident(iid)
    if i: i["status"]="Resolved"; flash(f"{i['location']} has been marked as resolved.")
    return redirect(request.referrer or url_for("dashboard"))

@app.route("/assign/<int:iid>",methods=["GET","POST"])
def assign_officer(iid):
    if not logged_in(): return redirect(url_for("login"))
    i=get_incident(iid)
    if not i: return redirect(url_for("incidents"))
    if request.method=="POST":
        i["officer"]=request.form.get("officer"); i["status"]="Officer Assigned"; flash(f"{i['officer']} assigned to {i['location']}.")
        return redirect(url_for("view_incident",iid=iid))
    body=render_template_string("""<div class="heading"><div><h1>Assign Officer 👮</h1><p>{{i.location}}</p></div></div><div class="panel"><form method="POST"><div class="form"><div class="field"><label>SELECT OFFICER</label><select name="officer">{% for o in officers %}<option value="{{o.name}}">{{o.name}} — {{o.department}}</option>{% endfor %}</select></div><div class="field"><label>INCIDENT</label><input value="{{i.location}}" disabled></div><div class="field full"><button class="btn" type="submit">👮 Assign Officer</button></div></div></form></div>""",i=i,officers=OFFICERS)
    return render_template_string(PAGE,title="Assign Officer",logged=True,page="officers",body=body)

@app.route("/officers")
def officers():
    if not logged_in(): return redirect(url_for("login"))
    active=sum(o["status"]=="Active" for o in OFFICERS); available=sum(o["status"]=="Available" for o in OFFICERS)
    body=render_template_string("""<div class="heading"><div><h1>Field Officers 👮</h1><p>Manage emergency response personnel.</p></div></div><div class="stats"><div class="card"><div class="card-title">TOTAL OFFICERS</div><div class="number">{{total}}</div></div><div class="card"><div class="card-title">ACTIVE</div><div class="number">{{active}}</div></div><div class="card"><div class="card-title">AVAILABLE</div><div class="number">{{available}}</div></div><div class="card"><div class="card-title">RESPONSE TEAM</div><div class="number">🚨</div></div></div><div class="panel"><table><tr><th>OFFICER</th><th>DEPARTMENT</th><th>AREA</th><th>STATUS</th><th>ACTION</th></tr>{% for o in officers %}<tr><td>👤 <b>{{o.name}}</b></td><td>{{o.department}}</td><td>{{o.area}}</td><td><span class="badge {% if o.status=='Available' %}low{% else %}medium{% endif %}">{{o.status}}</span></td><td><a class="btn gray" href="{{url_for('toggle_officer',oid=o.id)}}">Toggle Status</a></td></tr>{% endfor %}</table></div>""",officers=OFFICERS,total=len(OFFICERS),active=active,available=available)
    return render_template_string(PAGE,title="Officers",logged=True,page="officers",body=body)

@app.route("/toggle-officer/<int:oid>")
def toggle_officer(oid):
    if not logged_in(): return redirect(url_for("login"))
    o=next((x for x in OFFICERS if x["id"]==oid),None)
    if o: o["status"]="Available" if o["status"]=="Active" else "Active"; flash(f"{o['name']} status updated.")
    return redirect(url_for("officers"))

@app.route("/warnings")
def warnings():
    if not logged_in(): return redirect(url_for("login"))
    body=render_template_string("""<div class="heading"><div><h1>Public Warnings 🚨</h1><p>Prepare safety warnings for people near dangerous roads.</p></div></div>{% for w in warnings %}<div class="warning"><b>⚠️ {{w.location}} — {{w.risk}} RISK</b><br><br>{{w.message}}<br><br><span class="badge {{w.risk.lower()}}">{{w.status}}</span></div>{% endfor %}<div class="panel"><div class="panel-head"><b>Generate Warning</b></div><table><tr><th>LOCATION</th><th>RISK</th><th>ACTION</th></tr>{% for i in incidents %}{% if i.risk=="HIGH" %}<tr><td>📍 {{i.location}}</td><td><span class="badge high">HIGH</span></td><td><a class="btn red" href="{{url_for('publish_warning',iid=i.id)}}">📢 Publish Warning</a></td></tr>{% endif %}{% endfor %}</table></div>""",warnings=WARNINGS,incidents=INCIDENTS)
    return render_template_string(PAGE,title="Public Warnings",logged=True,page="warnings",body=body)

@app.route("/publish/<int:iid>")
def publish_warning(iid):
    if not logged_in(): return redirect(url_for("login"))
    i=get_incident(iid)
    if i:
        if not any(w["location"]==i["location"] for w in WARNINGS):
            WARNINGS.append({"location":i["location"],"risk":i["risk"],"message":f"⚠️ Public safety alert: Avoid {i['location']} due to reported flooding. Follow local authority instructions.","status":"Published"})
            flash(f"Public warning prepared for {i['location']}.")
        else: flash("A warning already exists for this location.")
    return redirect(url_for("warnings"))

@app.route("/analytics")
def analytics():
    if not logged_in(): return redirect(url_for("login"))
    total=len(INCIDENTS); high=sum(i["risk"]=="HIGH" for i in INCIDENTS); medium=sum(i["risk"]=="MEDIUM" for i in INCIDENTS); low=sum(i["risk"]=="LOW" for i in INCIDENTS)
    body=render_template_string("""<div class="heading"><div><h1>Analytics & Reports 📊</h1><p>Overview of current flood incidents.</p></div><button class="btn" onclick="window.print()">🖨️ Print Report</button></div><div class="stats"><div class="card"><div class="card-title">TOTAL</div><div class="number">{{total}}</div></div><div class="card"><div class="card-title">🔴 HIGH</div><div class="number">{{high}}</div></div><div class="card"><div class="card-title">🟡 MEDIUM</div><div class="number">{{medium}}</div></div><div class="card"><div class="card-title">🟢 LOW</div><div class="number">{{low}}</div></div></div><div class="panel"><div class="panel-head"><b>Risk Distribution</b></div><div style="padding:25px;line-height:2">🔴 HIGH — {{high}}<div style="height:18px;background:#ffe5e7;border-radius:10px"><div style="height:18px;width:{{(high/total*100) if total else 0}}%;background:#e33b45;border-radius:10px"></div></div><br>🟡 MEDIUM — {{medium}}<div style="height:18px;background:#fff1d0;border-radius:10px"><div style="height:18px;width:{{(medium/total*100) if total else 0}}%;background:#e3a51a;border-radius:10px"></div></div><br>🟢 LOW — {{low}}<div style="height:18px;background:#e5f7ec;border-radius:10px"><div style="height:18px;width:{{(low/total*100) if total else 0}}%;background:#16a05d;border-radius:10px"></div></div></div></div><div class="warning">ℹ️ <b>Prototype Notice:</b> This project currently uses manually entered/sample data. A real system would connect verified sensors, cameras, satellite information or authorized APIs.</div>""",total=total,high=high,medium=medium,low=low)
    return render_template_string(PAGE,title="Analytics",logged=True,page="analytics",body=body)

@app.route("/settings",methods=["GET","POST"])
def settings():
    if not logged_in(): return redirect(url_for("login"))
    if request.method=="POST":
        SETTINGS["authority"]=request.form.get("authority",SETTINGS["authority"])
        try:
            SETTINGS["high"]=int(request.form.get("high",35)); SETTINGS["medium"]=int(request.form.get("medium",15))
            flash("Settings saved successfully.")
        except ValueError: flash("Please enter valid numbers.")
    body=render_template_string("""<div class="heading"><div><h1>Settings ⚙️</h1><p>Configure AquaShield AI risk thresholds.</p></div></div><div class="panel"><form method="POST"><div class="form"><div class="field full"><label>AUTHORITY NAME</label><input name="authority" value="{{s.authority}}"></div><div class="field"><label>HIGH RISK WATER LEVEL (CM)</label><input type="number" name="high" value="{{s.high}}"></div><div class="field"><label>MEDIUM RISK WATER LEVEL (CM)</label><input type="number" name="medium" value="{{s.medium}}"></div><div class="field full"><button class="btn" type="submit">💾 Save Settings</button></div></div></form></div>""",s=SETTINGS)
    return render_template_string(PAGE,title="Settings",logged=True,page="settings",body=body)

@app.route("/help")
def help_page():
    if not logged_in(): return redirect(url_for("login"))
    body="""<div class="heading"><div><h1>Help & Support ❓</h1><p>Understand the AquaShield AI workflow.</p></div></div><div class="tiles"><div class="tile"><h3>🧠 Risk Calculation</h3><p>Water level is used as a simple rule-based indicator. High water level produces HIGH risk, medium level produces MEDIUM risk, and lower level produces LOW risk.</p></div><div class="tile"><h3>🚨 High Risk Response</h3><p>Authorities can review the incident, assign officers and prepare a public safety warning.</p></div><div class="tile"><h3>🌊 Project Flow</h3><p>Flood Report → Risk Analysis → Authority Alert → Officer Assignment → Public Warning → Resolution.</p></div></div><div class="panel"><div class="panel-head"><b>🛡️ AquaShield AI Workflow</b></div><div style="padding:22px;font-size:15px;line-height:2.2">🌧️ Detect / Report Flood<br>↓<br>🧠 Analyze Water Level<br>↓<br>🔴 Identify Dangerous Roads<br>↓<br>👮 Notify Authority / Officer<br>↓<br>📢 Warn Public<br>↓<br>✓ Resolve & Monitor</div></div>"""
    return render_template_string(PAGE,title="Help",logged=True,page="help",body=body)

if __name__ == "__main__":
    print("AquaShield AI starting...")
    print("Open http://127.0.0.1:5000")
    print("Demo login: admin / admin123")
    app.run(host="127.0.0.1",port=5000,debug=True)
