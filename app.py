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
    body { margin:0; padding:28px; min-height:100vh; font-family: "Segoe UI", Roboto, sans-serif; background: var(--bg1); color: #0f172a; }
    .wrap { max-width:1200px; margin:0 auto; }
    h1.app-title { font-weight: 900; color: var(--primary); font-size: 4rem; text-align: center; margin: 6px 0 20px 0; }
    .topbar { display:flex; justify-content:space-between; align-items:center; gap:12px; margin-bottom:18px; flex-wrap:wrap; }
    .admin-status { font-weight:800; display:flex; gap:10px; align-items:center; }
    .admin-pill { padding:8px 12px; border-radius:999px; background:#fde68a; color:#92400e; font-weight:800; }
    .controls { display:flex; gap:10px; align-items:center; }
    .btn { background:var(--accent); color:white; border:none; padding:10px 14px; border-radius:10px; font-weight:800; cursor:pointer; }
    .btn.secondary { background:white; color:var(--accent); border:2px solid rgba(37,99,235,0.12); }
    .btn.ghost { background:transparent; color:var(--accent); border:none; text-decoration:underline; padding:6px; font-weight:700; }
    .summary { display:flex; gap:14px; justify-content:center; flex-wrap:wrap; margin-bottom:18px; }
    .kpi { width:180px; height:120px; border-radius:14px; display:flex; flex-direction:column; justify-content:center; align-items:center; color:white; font-weight:800; cursor:pointer; }
    .kpi.all { background: linear-gradient(45deg,#475569,#334155); }
    .kpi.down { background: linear-gradient(45deg,#dc2626,#b91c1c); }
    .kpi.running { background: linear-gradient(45deg,#059669,#10b981); }
    .table-wrapper { background:#ffffffdd; padding:10px; border-radius:12px; overflow-x:auto; }
    table { width:100%; border-collapse: separate; border-spacing:0 10px; min-width:800px; }
    th { background:var(--accent); color:white; padding:12px 14px; text-align:left; font-weight:800; }
    td { background:white; padding:12px 14px; color:#0f172a; vertical-align:middle; font-weight:700; }
    .status-badge { padding:6px 14px; border-radius:999px; color:white; font-weight:900; }
    .status-down { background:#b91c1c; }
    .status-running { background:#059669; }
    .detail-link { background:none; border:none; color:var(--accent); text-decoration:underline; font-weight:900; cursor:pointer; }
    .modal-overlay { position:fixed; inset:0; background:rgba(2,6,23,0.45); display:none; align-items:center; justify-content:center; z-index:9999; }
    .modal-overlay.active { display:flex; }
    .modal { width:100%; max-width:880px; background:white; border-radius:12px; padding:18px; max-height:88vh; overflow:auto; position:relative; }
    .update-item { background:#f1f9ff; padding:10px 12px; border-radius:8px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center; }
    .icon-btn { background:none; border:none; cursor:pointer; font-size:1.2rem; margin-left:6px; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1 class="app-title">Report Problem Aesthetic</h1>
    <div class="topbar">
      <div class="admin-status" id="admin-status"></div>
      <div class="controls">
        <button class="btn" id="add-problem-btn">➕ Add Problem</button>
        <button class="btn secondary" id="admin-toggle-btn">🔑 Admin Mode</button>
      </div>
    </div>
    <div class="summary" id="summary"></div>
    <div class="table-wrapper">
      <table id="machine-table"></table>
    </div>
  </div>

  <!-- Admin Login Modal -->
  <div class="modal-overlay" id="admin-modal">
    <div class="modal">
      <button style="position:absolute;right:12px;top:8px;" id="admin-close">&times;</button>
      <h2>Admin Login</h2>
      <div><input id="admin-pin" type="password" placeholder="Enter PIN" />
      <button class="btn" id="admin-login-btn">Login</button></div>
    </div>
  </div>

  <!-- Problem Form Modal -->
  <div class="modal-overlay" id="problem-form-modal">
    <div class="modal">
      <button style="position:absolute;right:12px;top:8px;" id="problem-form-close">&times;</button>
      <h2 id="form-title">Add / Edit Problem</h2>
      <div id="form-body">
        <div><label>Customer</label><input id="f-customer" type="text" /></div>
        <div><label>Unit</label><input id="f-unit" type="text" /></div>
        <div><label>Status</label><select id="f-status"><option>Down</option><option>Running</option></select></div>
        <div><label>Reported Date</label><input id="f-date" type="date" /></div>
        <div><label>PIC</label><input id="f-pic" type="text" /></div>
        <div><label>Initial Update</label><textarea id="f-initial"></textarea></div>
        <button class="btn" id="form-submit">Submit</button>
      </div>
    </div>
  </div>

  <!-- Detail Modal -->
  <div class="modal-overlay" id="detail-modal">
    <div class="modal">
      <button style="position:absolute;right:12px;top:8px;" id="detail-close">&times;</button>
      <h2>History</h2>
      <div id="detail-body"></div>
    </div>
  </div>

<script>
  if (!localStorage.getItem('machines_demo')) {
    const defaultData = [
      { id:1, customer:'Klinik Aura', machine_name:'Lutronic Spectra XT', status:'Down', reported_date:'2023-10-01', pic:'Rully', updates:[
        { ts:'2023-10-02', author:'Rully', message:'Initial report: machine not powering on.'}
      ]}
    ];
    localStorage.setItem('machines_demo', JSON.stringify(defaultData));
  }
  if (localStorage.getItem('admin_mode') === null) localStorage.setItem('admin_mode','false');
  function load(){return JSON.parse(localStorage.getItem('machines_demo'));}
  function save(arr){localStorage.setItem('machines_demo',JSON.stringify(arr));}
  function isAdmin(){return localStorage.getItem('admin_mode')==='true';}
  function renderAdminStatus(){document.getElementById('admin-status').innerHTML=isAdmin()?'<div class="admin-pill">Admin Mode: ON</div>':'<div>User Mode</div>';}

  function renderTable(){
    const data=load();let html=`<tr><th>ID</th><th>Customer</th><th>Unit</th><th>Status</th><th>Aging</th><th>Action Plan</th><th>History</th></tr>`;
    data.forEach(m=>{
      const last=(m.updates&&m.updates.length)?m.updates[m.updates.length-1].message:'-';
      html+=`<tr><td>${m.id}</td><td>${m.customer}</td><td>${m.machine_name}</td><td>${m.status}</td><td>0</td><td>${last}</td><td><button class="detail-link" data-id="${m.id}">History</button></td></tr>`;
    });
    document.getElementById('machine-table').innerHTML=html;
    document.querySelectorAll('.detail-link').forEach(b=>b.onclick=()=>openDetail(b.dataset.id));
  }

  function openDetail(id){
    const m=load().find(x=>x.id==id);if(!m)return;
    let html=`<div>Customer: ${m.customer}</div>`;
    html+=`<h3>Updates</h3>`;
    m.updates.forEach((u,i)=>{
      html+=`<div class="update-item">
        <div><b>${u.author}</b> - <span id="msg-${id}-${i}">${u.message}</span></div>
        ${isAdmin()?`<div>
          <button class="icon-btn" onclick="editUpdate(${id},${i})">✏️</button>
          <button class="icon-btn" onclick="delUpdate(${id},${i})">🗑️</button>
        </div>`:''}
      </div>`;
    });
    if(isAdmin()){html+=`<button class="btn" onclick="addUpdate(${id})">Add Update</button>
    <button class="btn secondary" onclick="if(confirm('Delete problem?')) delProblem(${id})">Delete Problem</button>`;}
    document.getElementById('detail-body').innerHTML=html;
    document.getElementById('detail-modal').classList.add('active');
  }

  function addUpdate(mid){
    const arr=load();const m=arr.find(x=>x.id==mid);
    const msg=prompt('New update message:');if(!msg)return;
    m.updates.push({ts:new Date().toISOString(),author:m.pic||'Unknown',message:msg});
    save(arr);openDetail(mid);renderTable();
  }

  function editUpdate(mid, idx) {
    const span = document.getElementById(`msg-${mid}-${idx}`);
    const arr = load();
    const m = arr.find(x => x.id == mid);
    const u = m.updates[idx];
    const oldMsg = u.message;
    span.outerHTML = `
      <div id="edit-box-${mid}-${idx}">
        <textarea id="edit-ta-${mid}-${idx}" style="width:100%;padding:6px;border:1px solid #ccc;border-radius:6px;">${oldMsg}</textarea>
        <div style="margin-top:6px;display:flex;gap:8px;">
          <button class="btn" onclick="saveEdit(${mid},${idx})">Save</button>
          <button class="btn secondary" onclick="cancelEdit(${mid},${idx},'${oldMsg.replace(/'/g,"&#39;")}')">Cancel</button>
        </div>
      </div>
    `;
  }

  function saveEdit(mid, idx) {
    const arr = load();
    const m = arr.find(x => x.id == mid);
    const ta = document.getElementById(`edit-ta-${mid}-${idx}`);
    if (!ta) return;
    m.updates[idx].message = ta.value;
    save(arr);
    openDetail(mid);
    renderTable();
  }

  function cancelEdit(mid, idx, oldMsg) {
    document.getElementById(`edit-box-${mid}-${idx}`).outerHTML =
      `<span id="msg-${mid}-${idx}">${oldMsg}</span>`;
  }

  function delUpdate(mid,idx){
    if(!confirm('Delete this update?'))return;
    const arr=load();const m=arr.find(x=>x.id==mid);
    m.updates.splice(idx,1);save(arr);openDetail(mid);renderTable();
  }

  function delProblem(mid){
    const arr=load().filter(x=>x.id!=mid);save(arr);
    document.getElementById('detail-modal').classList.remove('active');renderTable();
  }

  document.getElementById('admin-toggle-btn').onclick=()=>{if(isAdmin()){localStorage.setItem('admin_mode','false');renderAdminStatus();}else{document.getElementById('admin-modal').classList.add('active');}};
  document.getElementById('admin-login-btn').onclick=()=>{if(document.getElementById('admin-pin').value==='0101'){localStorage.setItem('admin_mode','true');document.getElementById('admin-modal').classList.remove('active');renderAdminStatus();}else alert('Wrong PIN');};
  document.getElementById('admin-close').onclick=()=>document.getElementById('admin-modal').classList.remove('active');
  document.getElementById('detail-close').onclick=()=>document.getElementById('detail-modal').classList.remove('active');
  renderAdminStatus();renderTable();
</script>
</body>
</html>
"""

st_html(HTML, height=1300, scrolling=True)
