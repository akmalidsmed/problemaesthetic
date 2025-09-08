import streamlit as st
import pandas as pd
import datetime
import io
from openpyxl import Workbook

st.set_page_config(page_title="Report Problem Aesthetic", page_icon="🛠️", layout="wide")

# ================== Helper ==================
def get_aging_days(reported_date):
    return (datetime.date.today() - reported_date).days

def export_to_excel(problems):
    wb = Workbook()
    ws = wb.active
    ws.title = "Problems"

    # Header
    ws.append(["Customer", "Unit", "Status", "Reported Date", "Aging (days)", "Action Plan", "All Updates"])

    for p in problems:
        action_plan = p["updates"][-1]["update"] if p["updates"] else ""
        updates_str = "\n".join([f"{u['date']} - {u['pic']}: {u['update']}" for u in p["updates"]])
        ws.append([
            p["customer"],
            p["unit"],
            p["status"],
            str(p["reported_date"]),
            (datetime.date.today() - p["reported_date"]).days,
            action_plan,
            updates_str
        ])

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream

# ================== Session State ==================
if "problems" not in st.session_state:
    st.session_state["problems"] = []

if "admin_mode" not in st.session_state:
    st.session_state["admin_mode"] = False

# ================== UI ==================
st.markdown("<h1 style='text-align:center; font-size:40px;'>Report Problem Aesthetic</h1>", unsafe_allow_html=True)

# ---- Admin Mode ----
if not st.session_state["admin_mode"]:
    with st.expander("🔑 Admin Login"):
        pin = st.text_input("Enter PIN", type="password")
        if st.button("Login"):
            if pin == "0101":
                st.session_state["admin_mode"] = True
                st.success("Admin mode activated ✅")
            else:
                st.error("Invalid PIN ❌")
else:
    st.info("✅ Admin mode active")

# ---- Add Problem (Admin Only) ----
if st.session_state["admin_mode"]:
    with st.expander("➕ Add New Problem"):
        with st.form("add_problem_form"):
            customer = st.text_input("Customer")
            unit = st.text_input("Unit")
            status = st.selectbox("Status", ["Running", "Down"])
            reported_date = st.date_input("Reported Date", value=datetime.date.today())
            submit = st.form_submit_button("Add Problem")

            if submit:
                st.session_state["problems"].append({
                    "customer": customer,
                    "unit": unit,
                    "status": status,
                    "reported_date": reported_date,
                    "updates": []
                })
                st.success("Problem added!")

# ---- Main Table ----
if st.session_state["problems"]:
    df = pd.DataFrame([{
        "Customer": p["customer"],
        "Unit": p["unit"],
        "Status": p["status"],
        "Aging": get_aging_days(p["reported_date"]),
        "Action Plan": p["updates"][-1]["update"] if p["updates"] else "",
        "History": "📜 View"
    } for p in st.session_state["problems"]])

    st.dataframe(df, use_container_width=True, hide_index=True)

    # 📥 Download Excel
    excel_data = export_to_excel(st.session_state["problems"])
    st.download_button(
        label="📥 Download Data (Excel)",
        data=excel_data,
        file_name="problems_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("No problems reported yet.")
