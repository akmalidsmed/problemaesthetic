
import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime, timezone
from dateutil import tz

st.set_page_config(page_title="Aesthetic Machine Problem Monitor", page_icon="🛠️", layout="wide")

# ------------------ Styles ------------------
st.markdown("""
<style>
:root {
  --bg: #0b0f19;
  --card: #121826;
  --muted: #9aa4b2;
  --primary: #5b9cff;
  --success: #22c55e;
  --danger: #ef4444;
  --ring: rgba(91,156,255,.35);
}
html, body, [data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, #0b0f19, #0f172a) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
.card {
  background: var(--card);
  border: 1px solid rgba(255,255,255,.06);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,.25);
}
.kpi {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 4px;
  align-items: center;
}
.badge {
  padding: 2px 8px; border-radius: 999px; font-size: .8rem;
  border: 1px solid rgba(255,255,255,.08);
  background: rgba(255,255,255,.04);
}
.status {
  font-weight: 600;
  padding: 4px 10px; border-radius: 999px; font-size: .85rem;
}
.status.Running { background: rgba(34,197,94,.1); color: #86efac; border: 1px solid rgba(34,197,94,.25); }
.status.Down { background: rgba(239,68,68,.12); color: #fca5a5; border: 1px solid rgba(239,68,68,.25); }
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th, .table td {
  border-bottom: 1px solid rgba(255,255,255,.06);
  padding: 10px 8px;
  color: #e5e7eb;
  font-size: 0.95rem;
}
.table th { text-align: left; color: #cbd5e1; font-weight: 600; }
.chat {
  display: flex; flex-direction: column; gap: 10px;
  max-height: 420px; overflow-y: auto; padding-right: 8px;
}
.chat-item {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 12px;
  align-items: start;
}
.chat-item time {
  font-size: .8rem; color: var(--muted);
}
.chat-bubble {
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 12px;
  padding: 10px 12px;
}
fieldset {
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 12px;
  padding: 12px 14px;
}
legend {
  color: #cbd5e1; padding: 0 6px; font-size: .9rem;
}
input, textarea, select {
  border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ DB helpers ------------------
@st.cache_resource(show_spinner=False)
def get_conn():
    return sqlite3.connect("data/app.db", check_same_thread=False)

def query_df(q, params=()):
    conn = get_conn()
    df = pd.read_sql_query(q, conn, params=params)
    return df

def exec_sql(q, params=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(q, params)
    conn.commit()
    return cur.lastrowid

def calc_aging_days(reported_iso):
    try:
        dt_obj = datetime.fromisoformat(reported_iso)
    except Exception:
        return None
    now = datetime.now(dt_obj.tzinfo) if dt_obj.tzinfo else datetime.now()
    delta = now - dt_obj
    return round(delta.total_seconds() / 86400, 1)

def human_ts(ts_iso):
    try:
        dt_obj = datetime.fromisoformat(ts_iso)
    except Exception:
        return ts_iso
    return dt_obj.strftime("%d %b %Y, %H:%M")

# ------------------ Sidebar Filters ------------------
st.sidebar.title("🔎 Filters")
machines_df = query_df("""
SELECT
  m.id, m.customer, m.machine_name, m.status, m.reported_date, m.pic
FROM machines m
""")

if not machines_df.empty:
    machines_df["aging_days"] = machines_df["reported_date"].apply(calc_aging_days)
else:
    machines_df["aging_days"] = []

customers = ["(All)"] + sorted(machines_df["customer"].unique().tolist())
pics = ["(All)"] + sorted(machines_df["pic"].unique().tolist())
status_opts = ["(All)", "Running", "Down"]

f_customer = st.sidebar.selectbox("Customer", customers)
f_status = st.sidebar.selectbox("Status", status_opts, index=0)
f_pic = st.sidebar.selectbox("PIC", pics)
f_search = st.sidebar.text_input("Search (customer / machine)", "")

filtered = machines_df.copy()
if f_customer != "(All)":
    filtered = filtered[filtered["customer"] == f_customer]
if f_status != "(All)":
    filtered = filtered[filtered["status"] == f_status]
if f_pic != "(All)":
    filtered = filtered[filtered["pic"] == f_pic]
if f_search:
    s = f_search.lower()
    filtered = filtered[filtered.apply(lambda r: s in str(r["customer"]).lower() or s in str(r["machine_name"]).lower(), axis=1)]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="card kpi"><div><div class="badge">Total Down</div><h2>🛑 {}</h2></div></div>'.format(
        (machines_df["status"] == "Down").sum()
    ), unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card kpi"><div><div class="badge">Total Running</div><h2>✅ {}</h2></div></div>'.format(
        (machines_df["status"] == "Running").sum()
    ), unsafe_allow_html=True)
with col3:
    avg_aging = round(filtered["aging_days"].mean(), 1) if not filtered.empty else 0
    st.markdown('<div class="card kpi"><div><div class="badge">Avg Aging (days)</div><h2>⏳ {}</h2></div></div>'.format(
        avg_aging
    ), unsafe_allow_html=True)
with col4:
    oldest = filtered["aging_days"].max() if not filtered.empty else 0
    st.markdown('<div class="card kpi"><div><div class="badge">Oldest Case (days)</div><h2>📅 {}</h2></div></div>'.format(
        0 if pd.isna(oldest) else int(oldest)
    ), unsafe_allow_html=True)

st.markdown("### 📋 Machine Problems")

if filtered.empty:
    st.info("No data match the filters.")
else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <table class="table">
      <thead>
        <tr>
          <th>ID</th><th>Customer</th><th>Machine</th><th>Status</th><th>Reported</th><th>Aging (days)</th><th>PIC</th>
        </tr>
      </thead>
      <tbody>
    """, unsafe_allow_html=True)
    for _, r in filtered.sort_values("aging_days", ascending=False).iterrows():
        st.markdown(f"""
        <tr>
          <td>{r['id']}</td>
          <td>{r['customer']}</td>
          <td>{r['machine_name']}</td>
          <td><span class="status {r['status']}">{r['status']}</span></td>
          <td>{human_ts(r['reported_date'])}</td>
          <td>{r['aging_days'] if pd.notna(r['aging_days']) else '-'}</td>
          <td>{r['pic']}</td>
        </tr>
        """, unsafe_allow_html=True)
    st.markdown("</tbody></table></div>", unsafe_allow_html=True)

st.markdown("### 💬 Problem Updates (Chat-style)")
selected_id = st.selectbox("Select a machine to view conversation", [int(x) for x in filtered["id"].tolist()] if not filtered.empty else [])
if selected_id:
    detail = machines_df[machines_df["id"] == selected_id].iloc[0]
    st.markdown(f"""
    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <h3 style="margin:0; color:#e5e7eb;">{detail['customer']} — {detail['machine_name']}</h3>
          <div class="badge">Reported: {human_ts(detail['reported_date'])}</div>
        </div>
        <div class="status {detail['status']}">{detail['status']}</div>
      </div>
    """, unsafe_allow_html=True)

    updates_df = query_df("""
    SELECT id, machine_id, ts, author, message FROM updates
    WHERE machine_id = ?
    ORDER BY ts ASC
    """, (int(selected_id),))

    st.markdown('<div class="chat">', unsafe_allow_html=True)
    if updates_df.empty:
        st.markdown('<div class="chat-item"><time>—</time><div class="chat-bubble">No updates yet.</div></div>', unsafe_allow_html=True)
    else:
        for _, u in updates_df.iterrows():
            st.markdown(f"""
            <div class="chat-item">
              <time>{human_ts(u["ts"])}</time>
              <div class="chat-bubble"><strong>{u["author"]}</strong><br/>{u["message"]}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown("### ➕ Add New Machine Problem")
with st.form("add_machine"):
    c1, c2 = st.columns(2)
    with c1:
        new_customer = st.text_input("Customer *")
        new_machine = st.text_input("Machine Name *")
        new_pic = st.text_input("PIC *")
    with c2:
        new_status = st.selectbox("Status *", ["Down", "Running"], index=0)
        new_reported = st.datetime_input("Reported Date & Time *", value=datetime.now())
    first_note = st.text_area("Initial Problem Description (first message) *", height=100, placeholder="Describe the issue...")
    submitted = st.form_submit_button("Create")
    if submitted:
        if not (new_customer and new_machine and new_pic and new_reported and first_note):
            st.error("Please complete all required fields (*)")
        else:
            rid = exec_sql(
                "INSERT INTO machines(customer, machine_name, status, reported_date, pic) VALUES (?,?,?,?,?)",
                (new_customer, new_machine, new_status, new_reported.isoformat(), new_pic)
            )
            exec_sql(
                "INSERT INTO updates(machine_id, ts, author, message) VALUES (?,?,?,?)",
                (rid, new_reported.isoformat(), new_pic, first_note)
            )
            st.success(f"Created machine #{rid} — conversation started.")
            st.rerun()

st.markdown("### 📝 Update Existing Problem")
with st.form("add_update"):
    up_id = st.selectbox("Machine", machines_df["id"].tolist() if not machines_df.empty else [])
    author = st.text_input("Your Name (PIC) *")
    msg = st.text_area("Update Message *", height=100, placeholder="Type the latest update...")
    now_ts = datetime.now()
    status_change = st.selectbox("Change Status?", ["No change", "Running", "Down"])
    submitted2 = st.form_submit_button("Add Update")
    if submitted2:
        if not (up_id and author and msg):
            st.error("Please complete all required fields (*)")
        else:
            exec_sql("INSERT INTO updates(machine_id, ts, author, message) VALUES (?,?,?,?)",
                     (int(up_id), now_ts.isoformat(), author, msg))
            if status_change in ("Running","Down"):
                exec_sql("UPDATE machines SET status = ?, pic = ? WHERE id = ?",
                         (status_change, author, int(up_id)))
            st.success("Update added.")
            st.rerun()

st.markdown("""
<div style="opacity:.7; margin-top:18px; text-align:center; font-size:.9rem;">
  Built with ❤️ — Chat-style updates like WhatsApp, dark dashboard UI.
</div>
""", unsafe_allow_html=True)
