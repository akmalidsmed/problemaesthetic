import streamlit as st
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="Machine Problem Monitor - Popup Detail", layout="wide")

HTML = r"""<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Report Problem Aesthetic</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {
      background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      color: #1e293b;
      min-height: 100vh;
      margin: 0;
      padding: 20px;
    }
    .container {
      max-width: 1100px;
      margin: 0 auto;
    }
    h1 {
      font-weight: 900;
      font-size: 2.2rem;
      text-align: center;
      margin-bottom: 18px;
      color: #1e40af;
      text-shadow: 1px 1px 3px rgba(0,0,0,0.06);
    }
    .top-row {
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:12px;
      margin-bottom: 18px;
      flex-wrap:wrap;
    }
    .summary {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items:center;
    }
    .summary-item {
      color: white;
      font-weight: 700;
      font-size: 1.05rem;
      box-shadow: 0 6px 15px rgba(0,0,0,0.12);
      user-select: none;
      text-align: center;
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      width: 150px;
      height: 110px;
      transition: transform 0.12s ease, box-shadow 0.12s ease, opacity 0.12s ease;
      padding: 12px;
      cursor: pointer;
      outline: none;
    }
    .summary-item[data-active="true"] {
      transform: translateY(-6px);
      box-shadow: 0 12px 22px rgba(0,0,0,0.18);
    }
    .summary-item.total-problem {
      background: linear-gradient(45deg, #64748b, #475569);
    }
    .summary-item.red {
      background: linear-gradient(45deg, #dc2626, #b91c1c);
    }
    .summary-item.green {
      background: linear-gradient(45deg, #059669, #10b981);
    }
    .summary-label {
      font-size: 0.95rem;
      opacity: 0.9;
      margin-bottom: 6px;
    }
    .summary-value {
      font-size: 1.6rem;
      line-height: 1;
    }

    .add-btn {
      background: #2563eb;
      color: white;
      border: none;
      padding: 10px 14px;
      border-radius: 10px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 8px 20px rgba(37,99,235,0.18);
    }
    .add-btn:hover { background: #1e40af; }

    /* Scrollable table wrapper */
    .table-wrapper {
      overflow-x: auto;
      margin-bottom: 30px;
      box-shadow: 0 2px 8px rgba(59, 130, 246, 0.12);
      border-radius: 12px;
      background: #f8fafc;
      padding: 10px;
    }

    table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0 10px;
      min-width: 700px;
    }
    th, td {
      padding: 12px 15px;
      text-align: left;
      font-weight: 600;
      color: #1e293b;
      vertical-align: middle;
      white-space: nowrap;
    }
    th {
      background: #3b82f6;
      color: white;
      border-radius: 10px;
      user-select: none;
    }
    tr {
      background: #ffffff;
      box-shadow: 0 2px 8px rgba(59, 130, 246, 0.06);
      border-radius: 8px;
      transition: background-color 0.18s ease;
    }
    tr:hover {
      background-color: #f1f9ff;
    }
    .status-badge {
      display: inline-block;
      padding: 6px 12px;
      border-radius: 9999px;
      font-weight: 700;
      font-size: 0.9rem;
      color: white;
      user-select: none;
      text-align: center;
      min-width: 70px;
      white-space: nowrap;
    }
    .status-down {
      background-color: #dc2626;
    }
    .status-running {
      background-color: #059669;
    }
    .detail-btn {
      background: none;
      border: none;
      color: #2563eb;
      font-weight: 700;
      text-decoration: underline;
      cursor: pointer;
      padding: 0;
      font-size: 1rem;
      user-select: none;
      white-space: nowrap;
    }

    /* Modal styles */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.45);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 1000;
    }
    .modal-overlay.active {
      display: flex;
    }
    .modal {
      background: white;
      border-radius: 12px;
      max-width: 700px;
      width: 94%;
      max-height: 86vh;
      overflow-y: auto;
      box-shadow: 0 12px 40px rgba(0,0,0,0.28);
      padding: 22px;
      position: relative;
    }
    .modal h2 {
      color: #1e40af;
      font-weight: 900;
      margin-bottom: 14px;
      font-size: 1.5rem;
    }
    .modal .detail-row {
      margin-bottom: 10px;
      font-size: 1.03rem;
      color: #1e293b;
    }
    .modal .detail-label {
      font-weight: 800;
      color: #2563eb;
      margin-right: 8px;
    }
    .modal .updates {
      margin-top: 16px;
      border-top: 2px solid #cfe8ff;
      padding-top: 12px;
    }
    .modal .update-item {
      background: #f0f9ff;
      border-radius: 8px;
      padding: 10px 14px;
      margin-bottom: 10px;
      box-shadow: inset 0 0 6px rgba(37,99,235,0.06);
      color: #1e293b;
      font-size: 1rem;
    }
    .modal .update-author {
      font-weight: 700;
      color: #2563eb;
    }
    .modal .update-time {
      font-size: 0.85rem;
      color: #3b82f6;
      margin-left: 8px;
    }
    .modal-close-btn {
      position: absolute;
      top: 12px;
      right: 12px;
      background: transparent;
      border: none;
      font-size: 1.4rem;
      font-weight: 700;
      color: #2563eb;
      cursor: pointer;
    }
    .modal-close-btn:hover { color: #1e40af; }

    .form-row { margin-bottom:10px; display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
    .form-row label { width:110px; font-weight:700; color:#1e40af; }
    .form-row input, .form-row select, .form-row textarea {
      flex:1; padding:8px 10px; border-radius:8px; border:1px solid #e2e8f0; font-size:1rem;
    }
    .save-btn { background:#059669; color:white; padding:8px 12px; border-radius:8px; border:none; font-weight:800; cursor:pointer; }
    .save-btn:hover { background:#047857; }

    @media (max-width: 640px) {
      .summary-item { width: 46%; height: 110px; }
      .top-row { flex-direction:column; align-items:stretch; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Report Problem Aesthetic</h1>

    <div class="top-row">
      <div class="summary" id="summary" role="tablist" aria-label="Summary filters"></div>
      <div style="display:flex; gap:8px; align-items:center;">
        <button class="add-btn" id="add-problem-btn" title="Add new problem">➕ Add Problem</button>
      </div>
    </div>

    <!-- Scrollable Table Wrapper -->
    <div class="table-wrapper" aria-label="List of machines with problems">
      <table id="machine-table" role="table" aria-live="polite"></table>
    </div>
  </div>

  <!-- Modal popup -->
  <div class="modal-overlay" id="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="modal-title" tabindex="-1">
    <div class="modal" role="document">
      <button class="modal-close-btn" id="modal-close-btn" aria-label="Close modal">&times;</button>
      <h2 id="modal-title">Machine Problem Details</h2>
      <div id="modal-content"></div>
    </div>
  </div>

  <!-- Add/Edit Modal -->
  <div class="modal-overlay" id="form-overlay" role="dialog" aria-modal="true" aria-labelledby="form-title" tabindex="-1">
    <div class="modal" role="document">
      <button class="modal-close-btn" id="form-close-btn" aria-label="Close form">&times;</button>
      <h2 id="form-title">Add / Edit Problem</h2>
      <div id="form-content">
        <div class="form-row"><label for="f-customer">Customer</label><input id="f-customer" /></div>
        <div class="form-row"><label for="f-unit">Unit</label><input id="f-unit" /></div>
        <div class="form-row"><label for="f-status">Status</label>
          <select id="f-status"><option>Down</option><option>Running</option></select>
        </div>
        <div class="form-row"><label for="f-date">Reported Date</label><input id="f-date" type="date" /></div>
        <div class="form-row"><label for="f-pic">PIC</label><input id="f-pic" /></div>
        <div class="form-row"><label for="f-update">Initial Update</label><textarea id="f-update" rows="3" placeholder="Ops note / initial update (optional)"></textarea></div>
        <div style="display:flex; gap:8px; justify-content:flex-end; margin-top:8px;">
          <button class="save-btn" id="form-save-btn">Save</button>
        </div>
      </div>
    </div>
  </div>

<script>
  // --- Initialize default data if not present ---
  if (!localStorage.getItem('machines')) {
    const machines = [
      { id: 1, customer: 'Klinik Aura', machine_name: 'Lutronic Spectra XT', status: 'Down', reported_date: '2023-10-01', pic: 'Rully Candra', updates: [
        { ts: '2023-10-02T09:00:00', author: 'Rully Candra', message: 'Initial report: machine not powering on.' },
        { ts: '2023-10-03T14:30:00', author: 'Technician A', message: 'Checked power supply, replaced fuse.' }
      ] },
      { id: 2, customer: 'RS BIH Sanur', machine_name: 'Cynosure Revlite', status: 'Running', reported_date: '2023-10-02', pic: 'Muhammad Lukmansyah', updates: [] },
      { id: 3, customer: 'Klinik Everglow', machine_name: 'Lumenis M22', status: 'Down', reported_date: '2023-10-03', pic: 'Denny Firmansyah', updates: [
        { ts: '2023-10-04T08:00:00', author: 'Denny Firmansyah', message: 'Laser calibration error detected.' }
      ] },
    ];
    localStorage.setItem('machines', JSON.stringify(machines));
  }

  // --- Utility functions ---
  function loadMachines() {
    return JSON.parse(localStorage.getItem('machines') || '[]');
  }

  function saveMachines(arr) {
    localStorage.setItem('machines', JSON.stringify(arr));
  }

  function formatDateOnly(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    if (isNaN(date)) {
      // if stored as YYYY-MM-DD as string, construct Date safely
      const parts = dateString.split('-');
      if (parts.length === 3) {
        return new Date(parts[0], parts[1]-1, parts[2]).toLocaleDateString();
      }
      return dateString;
    }
    return date.toLocaleDateString(undefined, { year: 'numeric', month: '2-digit', day: '2-digit' });
  }

  function calcAgingDays(reportedDate) {
    const now = new Date();
    const reported = new Date(reportedDate);
    const diff = now - reported;
    return Math.max(0, Math.floor(diff / (1000 * 60 * 60 * 24)));
  }

  function humanTs(ts) {
    const date = new Date(ts);
    if (isNaN(date)) return ts;
    return date.toLocaleString();
  }

  // Filter state
  let currentFilter = 'all'; // 'all' | 'Down' | 'Running'

  function renderSummary(machines) {
    const totalDown = machines.filter(m => m.status === 'Down').length;
    const totalRunning = machines.filter(m => m.status === 'Running').length;
    const totalProblem = machines.length;

    const summaryEl = document.getElementById('summary');
    summaryEl.innerHTML = '';

    const items = [
      { key: 'all', label: 'Total Problem', value: totalProblem, cls: 'total-problem' },
      { key: 'Down', label: 'Total Down', value: totalDown, cls: 'red' },
      { key: 'Running', label: 'Total Running', value: totalRunning, cls: 'green' },
    ];

    items.forEach(it => {
      const div = document.createElement('div');
      div.className = 'summary-item ' + it.cls;
      div.setAttribute('role','button');
      div.setAttribute('tabindex','0');
      div.setAttribute('data-key', it.key);
      div.setAttribute('data-active', currentFilter === it.key ? 'true' : 'false');
      div.innerHTML = `<div class="summary-label">${it.label}</div><div class="summary-value">${it.value}</div>`;
      div.addEventListener('click', () => {
        // toggle filter: click same again -> show all
        if (currentFilter === it.key) currentFilter = 'all';
        else currentFilter = it.key;
        // update active visuals
        document.querySelectorAll('.summary-item').forEach(si => si.setAttribute('data-active','false'));
        document.querySelectorAll('.summary-item').forEach(si => { if (si.getAttribute('data-key') === currentFilter) si.setAttribute('data-active','true'); });
        renderMachineTable(loadMachines());
      });
      div.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') div.click();
      });
      summaryEl.appendChild(div);
    });
  }

  function renderMachineTable(machines) {
    let filtered = machines;
    if (currentFilter === 'Down') filtered = machines.filter(m => m.status === 'Down');
    else if (currentFilter === 'Running') filtered = machines.filter(m => m.status === 'Running');

    const problemMachines = filtered.filter(m => m.status === 'Down' || m.status === 'Running');

    if (problemMachines.length === 0) {
      document.getElementById('machine-table').innerHTML = '<tr><td colspan="7" class="text-center font-semibold p-6">No machines found for this filter.</td></tr>';
      return;
    }

    let html = `
      <tr>
        <th>ID</th>
        <th>Customer</th>
        <th>Unit</th>
        <th>Status</th>
        <th>Aging (days)</th>
        <th>Action Plan</th>
        <th>Action</th>
      </tr>
    `;

    problemMachines.forEach(m => {
      const aging = calcAgingDays(m.reported_date);
      const statusClass = m.status.toLowerCase() === 'down' ? 'status-down' : 'status-running';

      let lastUpdate = 'No updates yet.';
      if (m.updates && m.updates.length > 0) {
        const sortedUpdates = m.updates.slice().sort((a,b) => new Date(b.ts) - new Date(a.ts));
        lastUpdate = sortedUpdates[0].message;
      }

      html += `
        <tr>
          <td>${m.id}</td>
          <td>${m.customer}</td>
          <td>${m.machine_name}</td>
          <td><span class="status-badge ${statusClass}">${m.status}</span></td>
          <td>${aging}</td>
          <td>${escapeHtml(lastUpdate)}</td>
          <td><button class="detail-btn" data-id="${m.id}" aria-label="View details for machine ${m.machine_name}">Detail</button></td>
        </tr>
      `;
    });

    document.getElementById('machine-table').innerHTML = html;

    // Attach event listeners for detail buttons
    document.querySelectorAll('.detail-btn').forEach(btn => {
      btn.addEventListener('click', () => openModal(btn.dataset.id));
    });
  }

  function escapeHtml(text) {
    if (!text) return '';
    return text.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
  }

  const modalOverlay = document.getElementById('modal-overlay');
  const modalContent = document.getElementById('modal-content');
  const modalCloseBtn = document.getElementById('modal-close-btn');

  function openModal(id) {
    const machines = loadMachines();
    const machine = machines.find(m => m.id == id);
    if (!machine) return;

    const aging = calcAgingDays(machine.reported_date);

    let updatesHTML = '';
    if (!machine.updates || machine.updates.length === 0) {
      updatesHTML = '<p>No updates yet.</p>';
    } else {
      // show newest first
      updatesHTML = machine.updates.slice().reverse().map(u => `
        <div class="update-item">
          <span class="update-author">${escapeHtml(u.author)}</span>
          <span class="update-time"> (${humanTs(u.ts)})</span>: ${escapeHtml(u.message)}
        </div>
      `).join('');
    }

    modalContent.innerHTML = `
      <div class="detail-row"><span class="detail-label">ID:</span> ${machine.id}</div>
      <div class="detail-row"><span class="detail-label">Customer:</span> ${escapeHtml(machine.customer)}</div>
      <div class="detail-row"><span class="detail-label">Unit:</span> ${escapeHtml(machine.machine_name)}</div>
      <div class="detail-row"><span class="detail-label">Status:</span> ${escapeHtml(machine.status)}</div>
      <div class="detail-row"><span class="detail-label">Reported Date:</span> ${formatDateOnly(machine.reported_date)}</div>
      <div class="detail-row"><span class="detail-label">Aging (days):</span> ${aging}</div>
      <div class="detail-row"><span class="detail-label">PIC:</span> ${escapeHtml(machine.pic)}</div>

      <div class="updates">
        <h3 class="detail-label mb-2">Updates:</h3>
        ${updatesHTML}
      </div>

      <div style="display:flex; gap:8px; justify-content:flex-end; margin-top:12px;">
        <button id="edit-btn" class="save-btn" style="background:#2563eb;">Edit</button>
      </div>
    `;

    // attach edit handler (asks for PIN then opens edit form)
    setTimeout(() => {
      const editBtn = document.getElementById('edit-btn');
      if (editBtn) {
        editBtn.addEventListener('click', () => {
          const userPin = prompt('Masukkan PIN untuk edit (4 digits):');
          if (userPin === null) return;
          if (userPin === '0101') {
            openForm('edit', machine.id);
            closeModal();
          } else {
            alert('PIN salah.');
          }
        });
      }
    }, 100);

    modalOverlay.classList.add('active');
    modalOverlay.focus();
  }

  function closeModal() {
    modalOverlay.classList.remove('active');
  }

  modalCloseBtn.addEventListener('click', closeModal);

  modalOverlay.addEventListener('click', e => {
    if (e.target === modalOverlay) closeModal();
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      if (modalOverlay.classList.contains('active')) closeModal();
      if (formOverlay.classList.contains('active')) closeForm();
    }
  });

  // --- Add/Edit form modal logic ---
  const addBtn = document.getElementById('add-problem-btn');
  const formOverlay = document.getElementById('form-overlay');
  const formCloseBtn = document.getElementById('form-close-btn');

  function openForm(mode='add', id=null) {
    // mode: 'add' or 'edit'
    const title = document.getElementById('form-title');
    const fCustomer = document.getElementById('f-customer');
    const fUnit = document.getElementById('f-unit');
    const fStatus = document.getElementById('f-status');
    const fDate = document.getElementById('f-date');
    const fPic = document.getElementById('f-pic');
    const fUpdate = document.getElementById('f-update');

    if (mode === 'add') {
      title.textContent = 'Add Problem';
      fCustomer.value = '';
      fUnit.value = '';
      fStatus.value = 'Down';
      // default to today
      const d = new Date();
      const iso = d.toISOString().slice(0,10);
      fDate.value = iso;
      fPic.value = '';
      fUpdate.value = '';
      formOverlay.classList.add('active');
      fCustomer.focus();
      formOverlay.dataset.mode = 'add';
      formOverlay.dataset.id = '';
    } else {
      // edit
      const machines = loadMachines();
      const machine = machines.find(m => m.id == id);
      if (!machine) return;
      title.textContent = 'Edit Problem';
      fCustomer.value = machine.customer || '';
      fUnit.value = machine.machine_name || '';
      fStatus.value = machine.status || 'Down';
      // if stored as YYYY-MM-DD or ISO
      let dt = machine.reported_date || '';
      if (!dt) {
        dt = new Date().toISOString().slice(0,10);
      } else {
        // try to make YYYY-MM-DD
        const d = new Date(dt);
        if (!isNaN(d)) dt = d.toISOString().slice(0,10);
      }
      fDate.value = dt;
      fPic.value = machine.pic || '';
      fUpdate.value = '';
      formOverlay.classList.add('active');
      formOverlay.dataset.mode = 'edit';
      formOverlay.dataset.id = id;
    }
  }

  function closeForm() {
    formOverlay.classList.remove('active');
  }

  addBtn.addEventListener('click', () => {
    openForm('add', null);
  });

  formCloseBtn.addEventListener('click', closeForm);
  formOverlay.addEventListener('click', e => { if (e.target === formOverlay) closeForm(); });

  // Save handler
  document.getElementById('form-save-btn').addEventListener('click', () => {
    const mode = formOverlay.dataset.mode || 'add';
    const id = formOverlay.dataset.id || null;
    const fCustomer = document.getElementById('f-customer').value.trim();
    const fUnit = document.getElementById('f-unit').value.trim();
    const fStatus = document.getElementById('f-status').value;
    const fDate = document.getElementById('f-date').value;
    const fPic = document.getElementById('f-pic').value.trim() || 'Unknown';
    const fUpdate = document.getElementById('f-update').value.trim();

    if (!fCustomer || !fUnit || !fDate) {
      alert('Mohon lengkapi Customer, Unit, dan Reported Date.');
      return;
    }

    const machines = loadMachines();

    if (mode === 'add') {
      // create new id
      const newId = machines.reduce((acc,m)=>Math.max(acc,m.id||0),0) + 1;
      const newMach = {
        id: newId,
        customer: fCustomer,
        machine_name: fUnit,
        status: fStatus,
        reported_date: fDate,
        pic: fPic,
        updates: []
      };
      if (fUpdate) {
        newMach.updates.push({ ts: new Date().toISOString(), author: fPic, message: fUpdate });
      }
      machines.push(newMach);
      saveMachines(machines);
      closeForm();
      renderAll();
    } else {
      // edit existing
      const mid = parseInt(id);
      const idx = machines.findIndex(m => m.id === mid);
      if (idx === -1) {
        alert('Data tidak ditemukan.');
        return;
      }
      machines[idx].customer = fCustomer;
      machines[idx].machine_name = fUnit;
      machines[idx].status = fStatus;
      machines[idx].reported_date = fDate;
      machines[idx].pic = fPic;
      if (fUpdate) {
        machines[idx].updates = machines[idx].updates || [];
        machines[idx].updates.push({ ts: new Date().toISOString(), author: fPic, message: fUpdate });
      }
      saveMachines(machines);
      closeForm();
      renderAll();
    }
  });

  // Hook edit opening from outside (when PIN validated earlier)
  // We will re-use openForm('edit', id)

  // --- Initialize render function ---
  function renderAll() {
    const machines = loadMachines();
    renderSummary(machines);
    renderMachineTable(machines);
  }

  // initial render
  renderAll();

  // Expose some functions to global for access after prompt PIN flow
  window.openForm = openForm;
  window.renderAll = renderAll;

</script>
</body>
</html>
"""

# NOTE: removed the earlier small Streamlit markdown header per request (only HTML title used)
st_html(HTML, height=1100, scrolling=True)
