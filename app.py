import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime
from dateutil import tz
import os

st.set_page_config(page_title="Aesthetic Machine Problem Monitor", page_icon="🛠️", layout="wide")

# ------------------ Init DB ------------------
DB_FILE = "app.db"

def init_db():
    first = not os.path.exists(DB_FILE)
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS machines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer TEXT NOT NULL,
        machine_name TEXT NOT NULL,
        status TEXT CHECK(status IN ('Running','Down')) NOT NULL DEFAULT 'Down',
        reported_date TEXT NOT NULL,
        pic TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        machine_id INTEGER NOT NULL,
        ts TEXT NOT NULL,
        author TEXT NOT NULL,
        message TEXT NOT NULL,
        FOREIGN KEY(machine_id) REFERENCES machines(id) ON DELETE CASCADE
    );
    """)
    if first:
        now = datetime.now()
        machines = [
            ("Klinik Aura", "Lutronic Spectra XT", "Down", (now.replace(microsecond=0)).isoformat(), "Rully Candra"),
            ("RS BIH Sanur", "Cynosure Revlite", "Running", (now.replace(microsecond=0)).isoformat(), "Muhammad Lukmansyah"),
            ("Klinik Everglow", "Lumenis M22", "Down", (now.replace(microsecond=0)).isoformat(), "Denny Firmansyah"),
        ]
        cur.executemany("INSERT INTO machines(customer,machine_name,status,reported_date,pic) VALUES (?,?,?,?,?)", machines)
        conn.commit()
    return conn

conn = init_db()

# ------------------ Helpers ------------------
def query_df(q, params=()):
    return pd.read_sql_query(q, conn, params=params)

def exec_sql(q, params=()):
    cur = conn.cursor()
    cur.execute(q, params)
    conn.commit()
    return cur.lastrowid

def calc_aging_days(reported_iso):
    try:
        dt_obj = datetime.fromisoformat(reported_iso)
        delta = datetime.now() - dt_obj
        return round(delta.total_seconds() / 86400, 1)
    except:
        return None

def human_ts(ts_iso):
    try:
        return datetime.fromisoformat(ts_iso).strftime("%d %b %Y, %H:%M")
    except:
        return ts_iso

# ------------------ UI ------------------
st.title("🛠️ Aesthetic Machine Problem Monitor")

machines_df = query_df("SELECT * FROM machines")
machines_df["aging_days"] = machines_df["reported_date"].apply(calc_aging_days)

# KPI
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Down", (machines_df["status"]=="Down").sum())
col2.metric("Total Running", (machines_df["status"]=="Running").sum())
col3.metric("Avg Aging (days)", round(machines_df["aging_days"].mean(),1) if not machines_df.empty else 0)
col4.metric("Oldest Case (days)", int(machines_df["aging_days"].max()) if not machines_df.empty else 0)

# Tabel Mesin
st.subheader("📋 Machine Problems")
st.dataframe(machines_df[["id","customer","machine_name","status","reported_date","aging_days","pic"]])

# Chat-style updates
st.subheader("💬 Problem Updates")
machine_ids = machines_df["id"].tolist()
selected_id = st.selectbox("Select machine", machine_ids if machine_ids else [])
if selected_id:
    updates_df = query_df("SELECT * FROM updates WHERE machine_id=? ORDER BY ts ASC", (selected_id,))
    if updates_df.empty:
        st.info("No updates yet.")
    else:
        for _, u in updates_df.iterrows():
            st.markdown(f"**{u['author']}** ({human_ts(u['ts'])}): {u['message']}")

# Add Machine
st.subheader("➕ Add New Machine")
with st.form("add_machine"):
    customer = st.text_input("Customer")
    machine_name = st.text_input("Machine Name")
    status = st.selectbox("Status", ["Down","Running"])
    pic = st.text_input("PIC")
    note = st.text_area("Initial Problem Note")
    submitted = st.form_submit_button("Create")
    if submitted and all([customer,machine_name,status,pic,note]):
        now = datetime.now().isoformat()
        rid = exec_sql("INSERT INTO machines(customer,machine_name,status,reported_date,pic) VALUES (?,?,?,?,?)",
                       (customer,machine_name,status,now,pic))
        exec_sql("INSERT INTO updates(machine_id,ts,author,message) VALUES (?,?,?,?)",
                 (rid, now, pic, note))
        st.success("Machine added with first note.")
        st.experimental_rerun()

# Add Update
st.subheader("📝 Add Update")
with st.form("add_update"):
    up_id = st.selectbox("Machine ID", machine_ids)
    author = st.text_input("Your Name")
    msg = st.text_area("Update Message")
    new_status = st.selectbox("Change Status?", ["No change","Running","Down"])
    submitted2 = st.form_submit_button("Add Update")
    if submitted2 and all([up_id,author,msg]):
        now = datetime.now().isoformat()
        exec_sql("INSERT INTO updates(machine_id,ts,author,message) VALUES (?,?,?,?)",(up_id,now,author,msg))
        if new_status in ("Running","Down"):
            exec_sql("UPDATE machines SET status=?, pic=? WHERE id=?",(new_status,author,up_id))
        st.success("Update added.")
        st.experimental_rerun()
