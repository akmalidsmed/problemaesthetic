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
  <!-- SheetJS for Excel export -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
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
    .btn.success { background:#059669; color:white; box-shadow:0 10px 24px rgba(5,150,105,0.12); }

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
      </div>

    <div class="summary" id="summary" role="tablist" aria-label="summary filters"></div>

  <div class="wrap">

    <div class="topbar">
      <div class="admin-status" id="admin-status">
        <!-- Admin pill will be inserted here -->
      </div>

      <div class="controls">
        <button class="btn success" id="export-excel-btn">📊 Export to Excel</button>
        <button class="btn" id="add-problem-btn">➕ Add Problem</button>
        <button class="btn secondary" id="admin-toggle-btn">🔑 Admin Mode</button>
        <button class="btn ghost" id="clear-data-btn"></button>
      </div>
    </div>
    
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
      <div class="small muted-plain"><strongstrong></div>
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

  // Excel Export Function
  function exportToExcel() {
    const data = load();
    if (data.length === 0) {
      alert('No data to export');
      return;
    }

    // Create workbook
    const wb = XLSX.utils.book_new();
    
    // Summary Sheet
    const summaryData = [
      ['Machine Problem Report Summary', '', '', ''],
      ['Generated Date:', new Date().toLocaleDateString(), '', ''],
      ['', '', '', ''],
      ['Category', 'Count', 'Percentage', ''],
      ['Total Problems', data.length, '100%', ''],
      ['Down Machines', data.filter(d => d.status === 'Down').length, `${((data.filter(d => d.status === 'Down').length / data.length) * 100).toFixed(1)}%`, ''],
      ['Running Machines', data.filter(d => d.status === 'Running').length, `${((data.filter(d => d.status === 'Running').length / data.length) * 100).toFixed(1)}%`, ''],
    ];
    const summaryWs = XLSX.utils.aoa_to_sheet(summaryData);
    
    // Style summary sheet
    summaryWs['!merges'] = [
      { s: { r: 0, c: 0 }, e: { r: 0, c: 3 } }
    ];
    XLSX.utils.book_append_sheet(wb, summaryWs, 'Summary');

    // Main Data Sheet
    const mainData = [
      ['ID', 'Customer', 'Machine/Unit', 'Status', 'Reported Date', 'Aging (Days)', 'PIC', 'Latest Update', 'Total Updates']
    ];
    
    data.forEach(machine => {
      const latestUpdate = machine.updates && machine.updates.length > 0 ? 
        machine.updates[machine.updates.length - 1].message : 'No updates yet';
      
      mainData.push([
        machine.id,
        machine.customer || '',
        machine.machine_name || '',
        machine.status || '',
        formatDate(machine.reported_date),
        agingDays(machine.reported_date),
        machine.pic || '',
        latestUpdate,
        machine.updates ? machine.updates.length : 0
      ]);
    });
    
    const mainWs = XLSX.utils.aoa_to_sheet(mainData);
    
    // Auto-size columns
    const maxWidth = [];
    mainData.forEach(row => {
      row.forEach((cell, idx) => {
        const cellLength = cell ? cell.toString().length : 0;
        maxWidth[idx] = Math.max(maxWidth[idx] || 0, cellLength);
      });
    });
    
    mainWs['!cols'] = maxWidth.map(w => ({ width: Math.min(w + 2, 50) }));
    XLSX.utils.book_append_sheet(wb, mainWs, 'Machine Problems');

    // Updates Detail Sheet
    const updatesData = [
      ['Machine ID', 'Customer', 'Machine/Unit', 'Update Date/Time', 'Author', 'Update Message']
    ];
    
    data.forEach(machine => {
      if (machine.updates && machine.updates.length > 0) {
        machine.updates.forEach(update => {
          updatesData.push([
            machine.id,
            machine.customer || '',
            machine.machine_name || '',
            update.ts ? formatUpdateDate(update.ts) : '',
            update.author || '',
            update.message || ''
          ]);
        });
      }
    });
    
    const updatesWs = XLSX.utils.aoa_to_sheet(updatesData);
    
    // Auto-size columns for updates sheet
    const updatesMaxWidth = [];
    updatesData.forEach(row => {
      row.forEach((cell, idx) => {
        const cellLength = cell ? cell.toString().length : 0;
        updatesMaxWidth[idx] = Math.max(updatesMaxWidth[idx] || 0, cellLength);
      });
    });
    
    updatesWs['!cols'] = updatesMaxWidth.map(w => ({ width: Math.min(w + 2, 60) }));
    XLSX.utils.book_append_sheet(wb, updatesWs, 'All Updates');

    // Down Machines Sheet (filtered)
    const downMachines = data.filter(d => d.status === 'Down');
    if (downMachines.length > 0) {
      const downData = [
        ['ID', 'Customer', 'Machine/Unit', 'Reported Date', 'Aging (Days)', 'PIC', 'Latest Update']
      ];
      
      downMachines.forEach(machine => {
        const latestUpdate = machine.updates && machine.updates.length > 0 ? 
          machine.updates[machine.updates.length - 1].message : 'No updates yet';
        
        downData.push([
          machine.id,
          machine.customer || '',
          machine.machine_name || '',
          formatDate(machine.reported_date),
          agingDays(machine.reported_date),
          machine.pic || '',
          latestUpdate
        ]);
      });
      
      const downWs = XLSX.utils.aoa_to_sheet(downData);
      const downMaxWidth = [];
      downData.forEach(row => {
        row.forEach((cell, idx) => {
          const cellLength = cell ? cell.toString().length : 0;
          downMaxWidth[idx] = Math.max(downMaxWidth[idx] || 0, cellLength);
        });
      });
      
      downWs['!cols'] = downMaxWidth.map(w => ({ width: Math.min(w + 2, 50) }));
      XLSX.utils.book_append_sheet(wb, downWs, 'Down Machines');
    }

    // Generate filename with timestamp
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const filename = `Machine_Problems_Report_${timestamp}.xlsx`;
    
    // Save file
    XLSX.writeFile(wb, filename);
    
    // Show success message
    alert(`Excel file exported successfully!\nFilename: ${filename}`);
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

  const clearBtn = document.getElementById('clear-data-btn');
  const exportExcelBtn = document.getElementById('export-excel-btn');

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

  // Table (History column shows last update message)
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
        <td><button class="detail-link" data-id="${m.id}">Click Here</button></td>
      </tr>`;
    });
  }
  table.innerHTML = html;

  // Attach detail handlers
  table.querySelectorAll('.detail-link').forEach(btn => {
    btn.addEventListener('click', ()=> openDetail(btn.dataset.id));
  });
}


  // Escape HTML
  function escapeHtml(s) {
    if (!s) return '';
    return s.toString().replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
  }

  // Open Detail Modal: show full info + admin controls (edit/add update/delete) when isAdmin
  function openDetail(id) {
    const data = load();
    const m = data.find(x=>x.id == id);
    if (!m) return;
    const body = document.getElementById('detail-body');
    let html = `
      <div class="row"><label>ID</label><div class="muted-plain">${m.id}</div></div>
      <div class="row"><label>Customer</label><div class="muted-plain">${escapeHtml(m.customer)}</div></div>
      <div class="row"><label>Unit</label><div class="muted-plain">${escapeHtml(m.machine_name)}</div></div>
      <div class="row"><label>Status</label><div class="muted-plain">${m.status}</div></div>
      <div class="row"><label>Reported Date</label><div class="muted-plain">${formatDate(m.reported_date)}</div></div>
      <div class="row"><label>PIC</label><div class="muted-plain">${escapeHtml(m.pic)}</div></div>
      <hr style="margin:12px 0;border:none;border-top:1px solid #eef4ff" />
      <h3 class="small">History (all updates)</h3>
      <div id="updates-list">`;
    if (m.updates && m.updates.length) {
      m.updates.slice().reverse().forEach((u, idx) => {
        // compute original index for delete mapping
        const origIndex = m.updates.length - 1 - idx;
        html += `<div class="update-item">
          <div>
            <div class="update-meta">${escapeHtml(u.author)} • ${escapeHtml(u.ts)}</div>
            <div class="update-left">${escapeHtml(u.message)}</div>
          </div>
          ${isAdmin() ? `<div style="display:flex;flex-direction:column;gap:8px;">
            <button class="btn secondary" data-action="edit-update" data-idx="${origIndex}" data-id="${m.id}">✏️</button>
            <button class="danger" data-action="del-update" data-idx="${origIndex}" data-id="${m.id}">🗑️</button>
          </div>` : ''}
        </div>`;
      });
    } else {
      html += `<div class="small muted-plain">No updates yet.</div>`;
    }
    html += `</div>`;

    // Admin action buttons in detail
    if (isAdmin()) {
      html += `<div style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px;">
        <button class="btn secondary" id="detail-edit-btn">Edit Problem</button>
        <button class="btn" id="detail-addupd-btn">Add Update</button>
        <button class="danger" id="detail-delete-btn">Delete Problem</button>
      </div>`;
    }
    body.innerHTML = html;
    detailModal.classList.add('active');

    // attach admin buttons
    if (isAdmin()) {
      document.getElementById('detail-edit-btn').addEventListener('click', ()=> openProblemForm('edit', m.id));
      document.getElementById('detail-addupd-btn').addEventListener('click', ()=> openAddUpdate(m.id));
      document.getElementById('detail-delete-btn').addEventListener('click', ()=> {
        if (!confirm('Delete this problem permanently?')) return;
        const arr = load().filter(x=>x.id!=m.id);
        save(arr); detailModal.classList.remove('active'); renderAll();
      });

      // attach delete/update edit handlers for each update button
      body.querySelectorAll('[data-action="del-update"]').forEach(btn=>{
        btn.addEventListener('click', ()=> {
          const idx = parseInt(btn.dataset.idx);
          const mid = parseInt(btn.dataset.id);
          if (!confirm('Delete this update?')) return;
          const arr = load();
          const mm = arr.find(x=>x.id==mid);
          if (!mm) return;
          mm.updates.splice(idx,1);
          save(arr); openDetail(mid); renderAll();
        });
      });
      body.querySelectorAll('[data-action="edit-update"]').forEach(btn=>{
        btn.addEventListener('click', ()=> {
          const idx = parseInt(btn.dataset.idx);
          const mid = parseInt(btn.dataset.id);
          openEditUpdate(mid, idx);
        });
      });
    }
  }

  // Open Add/Edit Problem Form (admin only). mode: 'add'|'edit'
  function openProblemForm(mode='add', id=null) {
    if (!isAdmin()) { alert('Admin mode required'); return; }
    const modal = problemModal;
    modal.classList.add('active');
    const title = document.getElementById('form-title');
    const cust = document.getElementById('f-customer');
    const unit = document.getElementById('f-unit');
    const status = document.getElementById('f-status');
    const date = document.getElementById('f-date');
    const pic = document.getElementById('f-pic');
    const initial = document.getElementById('f-initial');

    if (mode === 'add') {
      title.textContent = 'Add Problem';
      cust.value=''; unit.value=''; status.value='Down';
      date.value = new Date().toISOString().slice(0,10);
      pic.value=''; initial.value='';
      modal.dataset.mode='add'; modal.dataset.id='';
    } else {
      const arr = load(); const m = arr.find(x=>x.id==id);
      if(!m) return;
      title.textContent = 'Edit Problem';
      cust.value = m.customer || '';
      unit.value = m.machine_name || '';
      status.value = m.status || 'Down';
      // set yyyy-mm-dd
      let d = m.reported_date || new Date().toISOString().slice(0,10);
      const dt = new Date(d);
      if (!isNaN(dt)) d = dt.toISOString().slice(0,10);
      date.value = d;
      pic.value = m.pic || '';
      initial.value = '';
      modal.dataset.mode='edit'; modal.dataset.id = m.id;
    }
  }

  // Close modals
  document.getElementById('admin-close').addEventListener('click', ()=> { adminModal.classList.remove('active'); adminPinInput.value=''; });
  problemClose.addEventListener('click', ()=> problemModal.classList.remove('active'));
  formCancel.addEventListener('click', ()=> problemModal.classList.remove('active'));
  detailClose.addEventListener('click', ()=> detailModal.classList.remove('active'));

  // Admin toggle -> open admin modal
  adminToggle.addEventListener('click', ()=> {
    if (isAdmin()) {
      localStorage.setItem('admin_mode','false'); renderAll();
    } else {
      adminModal.classList.add('active');
      adminPinInput.value=''; adminPinInput.focus();
    }
  });

  // Admin login
  adminLoginBtn.addEventListener('click', ()=> {
    const pin = adminPinInput.value.trim();
    if (pin === '0101') {
      localStorage.setItem('admin_mode','true');
      adminModal.classList.remove('active');
      adminPinInput.value='';
      renderAll();
      alert('Admin Mode activated');
    } else {
      alert('PIN salah');
    }
  });

  // Add problem button => open form (not auto-add)
  addProblemBtn.addEventListener('click', ()=> {
    if (!isAdmin()) { alert('Admin Mode required to add problem'); return; }
    openProblemForm('add', null);
  });

  // Submit form (add or edit)
  formSubmit.addEventListener('click', ()=> {
    const mode = problemModal.dataset.mode || 'add';
    const id = problemModal.dataset.id || '';
    const cust = document.getElementById('f-customer').value.trim();
    const unit = document.getElementById('f-unit').value.trim();
    const status = document.getElementById('f-status').value;
    const date = document.getElementById('f-date').value;
    const pic = document.getElementById('f-pic').value.trim() || 'Unknown';
    const initial = document.getElementById('f-initial').value.trim();

    if (!cust || !unit || !date) { alert('Lengkapi Customer, Unit, dan Reported Date'); return; }

    const arr = load();
    if (mode === 'add') {
      const newId = uid();
      const newRec = { id: newId, customer: cust, machine_name: unit, status: status, reported_date: date, pic: pic, updates: [] };
      if (initial) newRec.updates.push({ ts: new Date().toISOString(), author: pic, message: initial });
      arr.push(newRec);
      save(arr);
      problemModal.classList.remove('active');
      renderAll();
    } else {
      const mid = parseInt(id);
      const idx = arr.findIndex(x=>x.id==mid);
      if (idx === -1) { alert('Data tidak ditemukan'); return; }
      arr[idx].customer = cust;
      arr[idx].machine_name = unit;
      arr[idx].status = status;
      arr[idx].reported_date = date;
      arr[idx].pic = pic;
      if (initial) arr[idx].updates.push({ ts: new Date().toISOString(), author: pic, message: initial });
      save(arr);
      problemModal.classList.remove('active');
      renderAll();
    }
  });

  // Add Update from detail view (modal sub-form)
  function openAddUpdate(mid) {
    if (!isAdmin()) { alert('Admin required'); return; }
    const arr = load(); const m = arr.find(x=>x.id==mid); if(!m) return;
    // Show a small inline prompt inside detail modal
    const body = document.getElementById('detail-body');
    const formHtml = `
      <div style="margin-top:12px;border-top:1px solid #f1f8ff;padding-top:12px;">
        <div class="row"><label>PIC</label><input id="tmp-upd-pic" type="text" value="${escapeHtml(m.pic)}" /></div>
        <div class="row"><label>Message</label><textarea id="tmp-upd-msg"></textarea></div>
        <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:8px;">
          <button class="btn secondary" id="tmp-upd-cancel">Cancel</button>
          <button class="btn" id="tmp-upd-save">Save Update</button>
        </div>
      </div>
    `;
    body.insertAdjacentHTML('beforeend', formHtml);
    document.getElementById('tmp-upd-cancel').addEventListener('click', ()=> { renderDetailInline(mid); });
    document.getElementById('tmp-upd-save').addEventListener('click', ()=> {
      const author = document.getElementById('tmp-upd-pic').value.trim() || m.pic || 'Unknown';
      const msg = document.getElementById('tmp-upd-msg').value.trim();
      if (!msg) { alert('Message tidak boleh kosong'); return; }
      m.updates = m.updates || [];
      m.updates.push({ ts: new Date().toISOString(), author: author, message: msg });
      save(arr);
      renderDetailInline(mid);
      renderAll(); // update table history
    });
  }

  // Render detail modal body again (used to refresh inline forms)
  function renderDetailInline(mid) {
    const data = load(); const m = data.find(x=>x.id==mid); if(!m) return;
    // reuse openDetail structure by closing and reopening to refresh
    detailModal.classList.remove('active');
    setTimeout(()=> openDetail(mid), 120);
  }

  // Edit update: open inline edit form for a specific update index
  function openEditUpdate(mid, updIndex) {
    if (!isAdmin()) return;
    const arr = load(); const m = arr.find(x=>x.id==mid); if(!m) return;
    const original = m.updates[updIndex];
    const body = document.getElementById('detail-body');
    const formHtml = `
      <div style="margin-top:12px;border-top:1px dashed #eef4ff;padding-top:12px;">
        <div class="row"><label>PIC</label><input id="edit-upd-pic" type="text" value="${escapeHtml(original.author)}"/></div>
        <div class="row"><label>Message</label><textarea id="edit-upd-msg">${escapeHtml(original.message)}</textarea></div>
        <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:8px;">
          <button class="btn secondary" id="edit-upd-cancel">Cancel</button>
          <button class="btn" id="edit-upd-save">Save Changes</button>
        </div>
      </div>`;
    body.insertAdjacentHTML('beforeend', formHtml);
    document.getElementById('edit-upd-cancel').addEventListener('click', ()=> { renderDetailInline(mid); });
    document.getElementById('edit-upd-save').addEventListener('click', ()=> {
      const a = document.getElementById('edit-upd-pic').value.trim() || m.pic || 'Unknown';
      const msg = document.getElementById('edit-upd-msg').value.trim();
      if (!msg) { alert('Message tidak boleh kosong'); return; }
      m.updates[updIndex].author = a;
      m.updates[updIndex].message = msg;
      // keep ts as original or update ts? we keep original ts for traceability
      save(arr);
      renderDetailInline(mid);
      renderAll();
    });
  }

  // Reset data (for demo) - confirmation
  clearBtn.addEventListener('click', ()=> {
    if (!confirm('Reset data ke default? Ini akan menghapus perubahan Anda.')) return;
    localStorage.removeItem('machines_demo');
    localStorage.removeItem('admin_mode');
    location.reload();
  });

  // Excel Export Event Listener
  exportExcelBtn.addEventListener('click', exportToExcel);

  // Search functionality
  searchInput.addEventListener('input', (e) => {
    currentSearch = e.target.value.trim();
    renderTable();
  });

  // Sort functionality
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('sort-btn')) {
      currentSort = e.target.dataset.sort;
      renderTable();
    }
  });

  // init render
  function renderAll() {
    renderAdminStatus();
    renderSummary();
    renderTable();
  }

  // wire detail modal close on overlay click / Esc
  document.getElementById('detail-modal').addEventListener('click', (e)=>{ if (e.target === document.getElementById('detail-modal')) detailModal.classList.remove('active'); });
  document.getElementById('problem-form-modal').addEventListener('click', (e)=>{ if (e.target === document.getElementById('problem-form-modal')) problemModal.classList.remove('active'); });
  document.getElementById('admin-modal').addEventListener('click', (e)=>{ if (e.target === document.getElementById('admin-modal')) adminModal.classList.remove('active'); });

  // initial call
  renderAll();

  // keyboard Esc to close modals
  document.addEventListener('keydown', (e)=> {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.active').forEach(m=>m.classList.remove('active'));
    }
  });
</script>
</body>
</html>
"""

st_html(HTML, height=1300, scrolling=True)
