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
    .update-left { font-weight:800; color:#0f172a; white-space: pre-wrap; }
    .update-meta { font-size:0.9rem; color:#2563eb; font-weight:900; margin-bottom:6px; }

    .danger { background:#fecaca; color:#7f1d1d; border-radius:8px; padding:8px 10px; font-weight:900; border:none; cursor:pointer; }
    .muted-plain { color:#475569; font-weight:800; }

    /* Buttons for inline edit */
    .update-item button {
      font-size: 1.2rem;
      line-height: 1;
      padding: 4px 8px;
      border-radius: 6px;
      border: none;
      cursor: pointer;
      user-select: none;
    }
    .update-item button:hover {
      opacity: 0.8;
    }

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
        <!-- Reset Data button removed -->
      </div>
    </div>

    <div class="summary" id="summary" role="tablist" aria-label="summary filters"></div>

    <div class="table-wrapper" aria-live="polite">
      <table id="machine-table" role="table"></table>
    </div>
  </div>

  <!-- Modals -->
  <!-- Admin Login Modal -->
  <div class="modal-overlay" id="admin-modal" aria-hidden="true">
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="admin-title">
      <button style="position:absolute;right:12px;top:8px;background:none;border:none;font-weight:900;color:var(--accent);cursor:pointer;" id="admin-close">&times;</button>
      <h2 id="admin-title">Admin Login</h2>
      <div class="row">
        <label for="admin-pin">Enter PIN</label>
        <input id="admin-pin" type="password" placeholder="4-digit PIN" />
        <button class="btn" id="admin-login-btn">Login</button>
      </div>
      <!-- PIN default text hidden -->
      <div class="small muted-plain" style="display:none;">PIN default: <strong>0101</strong> (only for demo). PIN input is hidden.</div>
    </div>
  </div>

  <!-- Add/Edit Problem Modal -->
  <div class="modal-overlay" id="problem-form-modal" aria-hidden="true">
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="form-title">
      <button style="position:absolute;right:12px;top:8px;background:none;border:none;font-weight:900;color:var(--accent);cursor:pointer;" id="problem-form-close">&times;</button>
      <h2 id="form-title">Add / Edit Problem</h2>
      <div id="form-body">
        <div class="row"><label>Customer</label><input id="f-customer" type="text" /></div>
        <div class="row"><label>Unit</label><input id="f-unit" type="text" /></div>
        <div class="row"><label>Status</label><select id="f-status"><option>Down</option><option>Running</option></select></div>
        <div class="row"><label>Reported Date</label><input id="f-date" type="date" /></div>
        <div class="row"><label>PIC</label><input id="f-pic" type="text" /></div>
        <div class="row"><label>Initial Update</label><textarea id="f-initial" placeholder="Optional initial update"></textarea></div>
        <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:8px;">
          <button class="btn secondary" id="form-cancel">Cancel</button>
          <button class="btn" id="form-submit">Submit</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Detail Modal -->
  <div class="modal-overlay" id="detail-modal" aria-hidden="true">
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="detail-title">
      <button style="position:absolute;right:12px;top:8px;background:none;border:none;font-weight:900;color:var(--accent);cursor:pointer;" id="detail-close">&times;</button>
      <h2 id="detail-title">Machine Problem Details</h2>
      <div id="detail-body"></div>
    </div>
  </div>

<script>
  // Initialize default data if absent
  if (!localStorage.getItem('machines_demo')) {
    const defaultData = [
      { id: 1, customer: 'Klinik Aura', machine_name: 'Lutronic Spectra XT', status: 'Down', reported_date: '2023-10-01', pic: 'Rully Candra', updates: [
        { ts: '2023-10-02T09:00:00', author: 'Rully Candra', message: 'Initial report: machine not powering on.' },
        { ts: '2023-10-03T14:30:00', author: 'Technician A', message: 'Checked power supply, replaced fuse.' }
      ]},
      { id: 2, customer: 'RS BIH Sanur', machine_name: 'Cynosure Revlite', status: 'Running', reported_date: '2023-10-02', pic: 'Muhammad Lukmansyah', updates: [
        { ts: '2023-10-05T09:00:00', author: 'Muhammad Lukmansyah', message: 'Routine check - all OK.' }
      ]}
    ];
    localStorage.setItem('machines_demo', JSON.stringify(defaultData));
  }

  if (localStorage.getItem('admin_mode') === null) localStorage.setItem('admin_mode','false');

  // Helpers
  function load() { return JSON.parse(localStorage.getItem('machines_demo')||'[]'); }
  function save(arr) { localStorage.setItem('machines_demo', JSON.stringify(arr)); }
  function isAdmin() { return localStorage.getItem('admin_mode') === 'true'; }
  function uid() { const arr=load(); return (arr.reduce((a,b)=>Math.max(a,b.id||0),0)+1); }
  function formatDate(d) {
    if(!d) return '';
    const parts = d.split('T')[0] || d;
    const dt = new Date(parts);
    if (!isNaN(dt)) return dt.toLocaleDateString();
    return d;
  }
  function agingDays(date) {
    const now = new Date(); const rep = new Date(date);
    const diff = now - rep;
    return Math.max(0, Math.floor(diff / (1000*60*60*24)));
  }

  // UI refs
  const adminStatusEl = document.getElementById('admin-status');
  const adminModal = document.getElementById('admin-modal');
  const adminPinInput = document.getElementById('admin-pin');
  const adminLoginBtn = document.getElementById('admin-login-btn');
  const adminToggle = document.getElementById('admin-toggle-btn');
  const adminClose = document.getElementById('admin-close');

  const addProblemBtn = document.getElementById('add-problem-btn');
  const problemModal = document.getElementById('problem-form-modal');
  const problemClose = document.getElementById('problem-form-close');
  const formCancel = document.getElementById('form-cancel');
  const formSubmit = document.getElementById('form-submit');

  const detailModal = document.getElementById('detail-modal');
  const detailClose = document.getElementById('detail-close');

  // Update admin status pill
  function renderAdminStatus() {
    if (isAdmin()) {
      adminStatusEl.innerHTML = '<div class="admin-pill">Admin Mode: ON</div>';
      adminToggle.textContent = '🚪 Logout Admin';
    } else {
      adminStatusEl.innerHTML = '<div class="muted-plain">Mode: User</div>';
      adminToggle.textContent = '🔑 Admin Mode';
    }
  }

  // Summary KPIs (clickable to filter)
  let currentFilter = 'all';
  function renderSummary() {
    const data = load();
    const total = data.length;
    const down = data.filter(d=>d.status==='Down').length;
    const running = data.filter(d=>d.status==='Running').length;
    const el = document.getElementById('summary');
    el.innerHTML = `
      <div class="kpi all" data-key="all" role="button" tabindex="0"><div class="label">Total Problem</div><div class="value">${total}</div></div>
      <div class="kpi down" data-key="Down" role="button" tabindex="0"><div class="label">Total Down</div><div class="value">${down}</div></div>
      <div class="kpi running" data-key="Running" role="button" tabindex="0"><div class="label">Total Running</div><div class="value">${running}</div></div>
    `;
    el.querySelectorAll('.kpi').forEach(k=>{
      k.addEventListener('click', ()=> {
        const key = k.dataset.key;
        if (currentFilter === key) currentFilter = 'all'; else currentFilter = key;
        renderTable();
      });
    });
  }

  // Table (Action Plan column shows last update message, History column is detail button)
  function renderTable() {
    const data = load();
    let list = data;
    if (currentFilter === 'Down') list = data.filter(x=>x.status==='Down');
    else if (currentFilter === 'Running') list = data.filter(x=>x.status==='Running');

    const table = document.getElementById('machine-table');
    let html = `<tr><th>ID</th><th>Customer</th><th>Unit</th><th>Status</th><th>Aging (days)</th><th>Action Plan</th><th>History</th></tr>`;
    if (list.length === 0) {
      html += `<tr><td colspan="7" class="small muted-plain" style="padding:24px;text-align:center">No machines found.</td></tr>`;
    } else {
      list.forEach(m => {
        const last = (m.updates && m.updates.length) ? m.updates[m.updates.length-1].message : 'No updates yet';
        html += `<tr>
          <td>${m.id}</td>
          <td>${escapeHtml(m.customer)}</td>
          <td>${escapeHtml(m.machine_name)}</td>
          <td><span class="status-badge ${m.status==='Down'?'status-down':'status-running'}">${m.status}</span></td>
          <td>${agingDays(m.reported_date)}</td>
          <td>${escapeHtml(last)}</td>
          <td><button class="detail-link" data-id="${m.id}">History</button></td>
        </tr>`;
      });
    }
    table.innerHTML = html;

    // Attach detail handlers
    table.querySelectorAll('.detail-link').forEach(btn => {
      btn.addEventListener('click', ()=> openDetail(btn.dataset.id));
    });
  }

 
