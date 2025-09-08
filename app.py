import streamlit as st
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="Report Problem Aesthetic", layout="wide")

HTML = r"""<!DOCTYPE html>
<html lang="en">
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
      font-size: 3.2rem;
      text-align: center;
      margin-bottom: 30px;
      color: #1e40af;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
    }
    .summary {
      display: flex;
      justify-content: center;
      gap: 20px;
      margin-bottom: 30px;
      flex-wrap: wrap;
    }
    .summary-item {
      color: white;
      font-weight: 700;
      font-size: 1.3rem;
      box-shadow: 0 6px 15px rgba(0,0,0,0.15);
      user-select: none;
      text-align: center;
      border-radius: 15px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      width: 160px;
      height: 160px;
      transition: transform 0.2s ease;
      padding: 20px;
      cursor: pointer;
    }
    .summary-item.total-problem { background: linear-gradient(45deg, #64748b, #475569); }
    .summary-item.red { background: linear-gradient(45deg, #dc2626, #b91c1c); }
    .summary-item.green { background: linear-gradient(45deg, #059669, #10b981); }
    .summary-item:hover { transform: scale(1.05); }

    .summary-label { font-size: 1rem; opacity: 0.9; margin-bottom: 8px; }
    .summary-value { font-size: 2.5rem; line-height: 1; }

    .actions-bar {
      text-align: right;
      margin-bottom: 20px;
    }
    .btn {
      background: #2563eb;
      color: white;
      font-weight: 700;
      border: none;
      padding: 10px 18px;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.2s ease;
      margin-left: 8px;
    }
    .btn:hover { background: #1e40af; }

    /* Table */
    .table-wrapper {
      overflow-x: auto;
      margin-bottom: 30px;
      box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
      border-radius: 12px;
      background: #f1f5f9;
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
    th { background: #3b82f6; color: white; border-radius: 12px; }
    tr {
      background: #f1f5f9;
      box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
      border-radius: 12px;
    }
    tr:hover { background-color: #bfdbfe; }

    .status-badge {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 9999px;
      font-weight: 700;
      font-size: 0.9rem;
      color: white;
    }
    .status-down { background-color: #dc2626; }
    .status-running { background-color: #059669; }

    .detail-btn, .edit-btn, .update-btn {
      background: none;
      border: none;
      color: #2563eb;
      font-weight: 700;
      text-decoration: underline;
      cursor: pointer;
      font-size: 0.95rem;
      margin-right: 6px;
    }
    .detail-btn:hover, .edit-btn:hover, .update-btn:hover { color: #1e40af; }

    /* Modal */
    .modal-overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.5);
      display: none; justify-content: center; align-items: center;
      z-index: 1000;
    }
    .modal-overlay.active { display: flex; }
    .modal {
      background: white;
      border-radius: 15px;
      max-width: 600px;
      width: 90%;
      max-height: 80vh;
      overflow-y: auto;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
      padding: 25px 30px;
      position: relative;
    }
    .modal h2 { color: #1e40af; font-weight: 900; margin-bottom: 20px; font-size: 1.8rem; }
    .modal .detail-row { margin-bottom: 12px; font-size: 1.1rem; color: #1e293b; }
    .modal .detail-label { font-weight: 700; color: #2563eb; }
    .modal-close-btn {
      position: absolute; top: 15px; right: 15px;
      background: transparent; border: none;
      font-size: 1.5rem; font-weight: 700; color: #2563eb;
      cursor: pointer;
    }
    .modal-close-btn:hover { color: #1e40af; }

    @media (max-width: 640px) {
      h1 { font-size: 2rem; }
      .summary-item { width: 80%; height: 140px; margin-bottom: 15px; }
      .summary-value { font-size: 2rem; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Report Problem Aesthetic</h1>

    <div class="actions-bar">
      <button class="btn" id="add-problem-btn">➕ Add Problem</button>
      <button class="btn" id="toggle-admin-btn">🔑 Admin Mode</button>
    </div>

    <!-- Summary KPIs -->
    <div class="summary" id="summary"></div>

    <!-- Table -->
    <div class="table-wrapper"><table id="machine-table"></table></div>
  </div>

  <!-- Modal -->
  <div class="modal-overlay" id="modal-overlay">
    <div class="modal">
      <button class="modal-close-btn" id="modal-close-btn">&times;</button>
      <h2 id="modal-title"></h2>
      <div id="modal-content"></div>
    </div>
  </div>

<script>
  if (!localStorage.getItem('machines')) {
    const machines = [
      { id: 1, customer: 'Klinik Aura', machine_name: 'Lutronic Spectra XT', status: 'Down', reported_date: '2023-10-01T10:00:00', pic: 'Rully Candra', updates: [] },
      { id: 2, customer: 'RS BIH Sanur', machine_name: 'Cynosure Revlite', status: 'Running', reported_date: '2023-10-02T11:00:00', pic: 'Muhammad Lukmansyah', updates: [] }
    ];
    localStorage.setItem('machines', JSON.stringify(machines));
  }

  if (!localStorage.getItem('adminMode')) localStorage.setItem('adminMode', 'false');
  let currentFilter = 'all';

  function loadMachines(){ return JSON.parse(localStorage.getItem('machines')||'[]'); }
  function saveMachines(m){ localStorage.setItem('machines', JSON.stringify(m)); }
  function adminMode(){ return localStorage.getItem('adminMode')==='true'; }

  function calcAgingDays(date){
    const diff = new Date()-new Date(date);
    return Math.floor(diff/86400000);
  }

  function renderSummary(machines){
    const totalDown = machines.filter(m=>m.status==='Down').length;
    const totalRunning = machines.filter(m=>m.status==='Running').length;
    const total = machines.length;
    document.getElementById('summary').innerHTML=`
      <div class="summary-item total-problem" data-filter="all">
        <div class="summary-label">Total Problem</div><div class="summary-value">${total}</div></div>
      <div class="summary-item red" data-filter="Down">
        <div class="summary-label">Total Down</div><div class="summary-value">${totalDown}</div></div>
      <div class="summary-item green" data-filter="Running">
        <div class="summary-label">Total Running</div><div class="summary-value">${totalRunning}</div></div>`;
    document.querySelectorAll('.summary-item').forEach(el=>{
      el.addEventListener('click', ()=>{ currentFilter=el.dataset.filter; render(); });
    });
  }

  function renderTable(machines){
    let list=machines;
    if(currentFilter!=='all'){ list=machines.filter(m=>m.status===currentFilter); }
    let html=`<tr><th>ID</th><th>Customer</th><th>Unit</th><th>Status</th><th>Aging</th><th>Action Plan</th><th>Action</th></tr>`;
    if(list.length===0){ html+=`<tr><td colspan="7" class="text-center p-6">No data.</td></tr>`; }
    list.forEach(m=>{
      const lastUpdate = m.updates.length?m.updates[m.updates.length-1].message:'No updates';
      html+=`<tr>
        <td>${m.id}</td><td>${m.customer}</td><td>${m.machine_name}</td>
        <td><span class="status-badge ${m.status==='Down'?'status-down':'status-running'}">${m.status}</span></td>
        <td>${calcAgingDays(m.reported_date)}</td><td>${lastUpdate}</td>
        <td>
          <button class="detail-btn" data-id="${m.id}">Detail</button>
          ${adminMode()?`<button class="edit-btn" data-id="${m.id}">Edit</button>
          <button class="update-btn" data-id="${m.id}">Add Update</button>`:''}
        </td></tr>`;
    });
    document.getElementById('machine-table').innerHTML=html;

    document.querySelectorAll('.detail-btn').forEach(btn=>btn.onclick=()=>openModal('detail',btn.dataset.id));
    if(adminMode()){
      document.querySelectorAll('.edit-btn').forEach(btn=>btn.onclick=()=>openModal('edit',btn.dataset.id));
      document.querySelectorAll('.update-btn').forEach(btn=>btn.onclick=()=>openModal('update',btn.dataset.id));
    }
  }

  const modalOverlay=document.getElementById('modal-overlay');
  const modalTitle=document.getElementById('modal-title');
  const modalContent=document.getElementById('modal-content');
  document.getElementById('modal-close-btn').onclick=()=>modalOverlay.classList.remove('active');

  function openModal(type,id){
    const machines=loadMachines(); const m=machines.find(x=>x.id==id);
    modalOverlay.classList.add('active');
    if(type==='detail'){
      modalTitle.textContent="Machine Problem Details";
      modalContent.innerHTML=`<div><b>ID:</b> ${m.id}</div>
        <div><b>Customer:</b> ${m.customer}</div>
        <div><b>Unit:</b> ${m.machine_name}</div>
        <div><b>Status:</b> ${m.status}</div>
        <div><b>Reported:</b> ${m.reported_date}</div>
        <div><b>PIC:</b> ${m.pic}</div>
        <div><b>Updates:</b><ul>${m.updates.map(u=>`<li>${u.ts} - ${u.author}: ${u.message}</li>`).join('')}</ul></div>`;
    }
    if(type==='edit'){
      modalTitle.textContent="Edit Machine";
      modalContent.innerHTML=`<label>Customer<input id="edit-cust" value="${m.customer}"/></label><br>
        <label>Unit<input id="edit-unit" value="${m.machine_name}"/></label><br>
        <label>Status<select id="edit-status"><option ${m.status==='Down'?'selected':''}>Down</option><option ${m.status==='Running'?'selected':''}>Running</option></select></label><br>
        <label>PIC<input id="edit-pic" value="${m.pic}"/></label><br>
        <button class="btn" id="save-edit">Save</button>`;
      document.getElementById('save-edit').onclick=()=>{
        m.customer=document.getElementById('edit-cust').value;
        m.machine_name=document.getElementById('edit-unit').value;
        m.status=document.getElementById('edit-status').value;
        m.pic=document.getElementById('edit-pic').value;
        saveMachines(machines); modalOverlay.classList.remove('active'); render();
      }
    }
    if(type==='update'){
      modalTitle.textContent="Add Update";
      modalContent.innerHTML=`<label>PIC<input id="upd-pic" value="${m.pic}"/></label><br>
        <label>Message<textarea id="upd-msg"></textarea></label><br>
        <button class="btn" id="save-upd">Save Update</button>`;
      document.getElementById('save-upd').onclick=()=>{
        const upd={ ts:new Date().toLocaleString(), author:document.getElementById('upd-pic').value, message:document.getElementById('upd-msg').value };
        m.updates.push(upd); saveMachines(machines); modalOverlay.classList.remove('active'); render();
      }
    }
  }

  document.getElementById('add-problem-btn').onclick=()=>{
    if(!adminMode()){alert("Admin mode required.");return;}
    const machines=loadMachines();
    const newId=machines.length?Math.max(...machines.map(m=>m.id))+1:1;
    const m={id:newId,customer:"New Customer",machine_name:"New Unit",status:"Down",reported_date:new Date().toISOString(),pic:"",updates:[]};
    machines.push(m); saveMachines(machines); render();
  };

  document.getElementById('toggle-admin-btn').onclick=()=>{
    if(adminMode()){ localStorage.setItem('adminMode','false'); alert("Logged out Admin Mode"); render(); return;}
    const pin=prompt("Enter PIN:",""); if(pin==="0101"){localStorage.setItem('adminMode','true'); alert("Admin Mode Activated"); render();}
    else alert("Wrong PIN");
  };

  function render(){ const machines=loadMachines(); renderSummary(machines); renderTable(machines); }
  render();
</script>
</body>
</html>
"""

st_html(HTML, height=1200, scrolling=True)
