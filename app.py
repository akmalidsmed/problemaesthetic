import streamlit as st
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="Report Problem Aesthetic", layout="wide")

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Report Problem Aesthetic</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root { --primary: #1e40af; --accent: #2563eb; --bg1: linear-gradient(135deg,#e0e7ff,#c7d2fe); }
    body {
      margin:0; padding:28px; min-height:100vh;
      font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: var(--bg1);
      color: #0f172a;
    }
    .wrap { max-width:1200px; margin:0 auto; }
    h1.app-title {
      font-weight: 900;
      color: var(--primary);
      font-size: 4rem; /* very large */
      text-align: center;
      margin: 6px 0 20px 0;
      letter-spacing: -1px;
      text-shadow: 2px 2px 8px rgba(0,0,0,0.08);
    }
    .topbar { display:flex; justify-content:space-between; align-items:center; gap:12px; margin-bottom:18px; flex-wrap:wrap; }
    .admin-status { font-weight:800; color:#0f172a; display:flex; gap:10px; align-items:center; }
    .admin-pill { padding:8px 12px; border-radius:999px; background:#fde68a; color:#92400e; font-weight:800; box-shadow:0 6px 18px rgba(250,204,21,0.12); }
    .controls { display:flex; gap:10px; align-items:center; }
    .btn { background:var(--accent); color:white; border:none; padding:10px 14px; border-radius:10px; font-weight:800; cursor:pointer; box-shadow:0 10px 24px rgba(37,99,235,0.12); }
    .btn.secondary { background:white; color:var(--accent); border:2px solid rgba(37,99,235,0.12); box-shadow:none; }
    .btn.ghost { background:transparent; color:var(--accent); border:none; text-decoration:underline; padding:6px; font-weight:700; }

    .summary { display:flex; gap:14px; justify-content:center; flex-wrap:wrap; margin-bottom:18px; }
    .kpi { width:180px; height:120px; border-radius:14px; display:flex; flex-direction:column; justify-content:center; align-items:center; color:white; font-weight:800; cursor:pointer; user-select:none; transition:transform .12s ease, box-shadow .12s ease; }
    .kpi:hover { transform:translateY(-6px); }
    .kpi .label { font-size:0.95rem; opacity:0.95; }
    .kpi .value { font-size:2rem; margin-top:6px; }

    .kpi.all { background: linear-gradient(45deg,#475569,#334155); }
    .kpi.down { background: linear-gradient(45deg,#dc2626,#b91c1c); }
    .kpi.running { background: linear-gradient(45deg,#059669,#10b981); }

    .table-wrapper { background:#ffffffdd; padding:10px; border-radius:12px; box-shadow:0 10px 40px rgba(2,6,23,0.06); overflow-x:auto; }
    table { width:100%; border-collapse: separate; border-spacing:0 10px; min-width:800px; }
    th { background:var(--accent); color:white; padding:12px 14px; text-align:left; font-weight:800; }
    td { background:white; padding:12px 14px; color:#0f172a; vertical-align:middle; font-weight:700; }
    tr td { box-shadow:0 6px 18px rgba(2,6,23,0.04); border-radius:8px; }
    .status-badge { padding:6px 14px; border-radius:999px; color:white; font-weight:900; }
    .status-down { background:#b91c1c; }
    .status-running { background:#059669; }

    .detail-link { background:none; border:none; color:var(--accent); text-decoration:underline; font-weight:900; cursor:pointer; }

    /* modal */
    .modal-overlay { position:fixed; inset:0; background:rgba(2,6,23,0.45); display:none; align-items:center; justify-content:center; z-index:9999; padding:16px; }
    .modal-overlay.active { display:flex; }
    .modal { width:100%; max-width:880px; background:white; border-radius:12px; padding:18px; max-height:88vh; overflow:auto; box-shadow:0 30px 80px rgba(2,6,23,0.25); position:relative; }
    .modal h2 { font-size:1.6rem; color:var(--primary); margin:0 0 12px 0; font-weight:900; }
    .modal .row { display:flex; gap:12px; align-items:center; margin-bottom:10px; flex-wrap:wrap; }
    .modal label { min-width:120px; font-weight:800; color:var(--accent); }
    .modal input[type="text"], .modal input[type="date"], .modal select, .modal textarea, .modal input[type="password"] {
      flex:1; padding:8px 10px; border:1px solid #e6eef8; border-radius:8px; font-size:1rem;
    }
    .modal textarea { min-height:90px; resize:vertical; }
    .modal .muted { font-weight:700; color:#475569; }
    .modal .small { font-size:0.95rem; color:#475569; }

    .update-item { background:#f1f9ff; padding:10px 12px; border-radius:8px; margin-bottom:8px; display:flex; justify-content:space-between; gap:8px; align-items:center; }
    .update-left { font-weight:800; color:#0f172a; }
    .update-meta { font-size:0.9rem; color:#2563eb; font-weight:900; margin-bottom:6px; }

    .danger { background:#fecaca; color:#7f1d1d; border-radius:8px; padding:8px 10px; font-weight:900; border:none; cursor:pointer; }
    .muted-plain { color:#475569; font-weight:800; }

    @media (max-width:720px) {
      h1.app-title { font-size:3rem; }
      .kpi { width:46%; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <h1 class="app-title">Report Problem Aesthetic</h1>

    <div class="topbar">
      <div class="admin-status" id="admin-status">
        <!-- Admin pill will be inserted here -->
      </div>

      <div class="controls">
        <button class="btn" id="add-problem-btn">➕ Add Problem</button>
        <button class="btn secondary" id="admin-toggle-btn">🔑 Admin Mode</button>
      </div>
    </div>

    <div class="summary" id="summary" role="tablist" aria-label="summary filters"></div>

    <div class="table-wrapper" aria-live="polite">
      <table id="machine-table" role="table"></table>
    </div>
  </div>

  <!-- Modals ... (tidak berubah) -->
  <!-- ... semua script JS tetap sama, hanya bagian clearBtn dihapus -->

<script>
  // ... semua kode JS tetap
  // 🔴 bagian clearBtn (reset data) sudah dihapus
</script>
</body>
</html>
"""

st_html(HTML, height=1300, scrolling=True)
