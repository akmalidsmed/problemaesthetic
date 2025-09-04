<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aesthetic Machine Problem Monitor</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background: linear-gradient(135deg,#f5f7fa,#c3cfe2); font-family: 'Segoe UI',sans-serif; }
    .container { max-width:1200px;margin:auto;padding:20px; }
    .section { background:#fff9;border-radius:10px;padding:20px;margin-bottom:20px;box-shadow:0 4px 6px rgba(0,0,0,.1);}
    .metric { text-align:center;margin:10px;padding:10px;border-radius:8px;}
    .metric.red{background:#f8d7da}.metric.green{background:#d4edda}
    table { width:100%;border-collapse:collapse }
    th,td{ padding:10px;border-bottom:1px solid #ddd;text-align:left }
    th{ background:#2980b9;color:white }
    .down{ background:#f8d7da}.running{ background:#d4edda }
    input,select,textarea{width:100%;padding:8px;margin:5px 0;border:1px solid #ccc;border-radius:5px;background:#eaf2f8}
    button{background:#2980b9;color:white;padding:10px 20px;border:none;border-radius:8px;cursor:pointer}
    button:hover{background:#3498db}
    .notif{background:#2ecc71;color:white;padding:10px;margin:10px 0;border-radius:5px;display:none}
  </style>
</head>
<body>
  <div class="container">
    <h1 class="text-2xl font-bold text-center mb-5">🛠️ Aesthetic Machine Problem Monitor</h1>

    <div id="notif" class="notif"></div>

    <div class="section">
      <h2>KPIs</h2>
      <div id="kpis" class="flex flex-wrap gap-2"></div>
    </div>

    <div class="section">
      <h2>Machine Problems</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th><th>Customer</th><th>Machine Name</th>
            <th>Status</th><th>Reported Date</th><th>Aging Days</th><th>PIC</th>
          </tr>
        </thead>
        <tbody id="machine-table"></tbody>
      </table>
    </div>

    <div class="section">
      <h2>Problem Updates</h2>
      <select id="machine-select"></select>
      <div id="updates" class="mt-2"></div>
    </div>

    <div class="section">
      <h2>Add New Machine</h2>
      <form id="add-machine-form">
        <input type="text" id="customer" placeholder="Customer" required>
        <input type="text" id="machine-name" placeholder="Machine Name" required>
        <select id="status"><option>Down</option><option>Running</option></select>
        <input type="text" id="pic" placeholder="PIC" required>
        <textarea id="init-note" placeholder="Initial Problem Note" required></textarea>
        <button type="submit">Create</button>
      </form>
    </div>

    <div class="section">
      <h2>Add Update</h2>
      <form id="add-update-form">
        <select id="update-machine-select" required></select>
        <input type="text" id="author" placeholder="Your Name" required>
        <textarea id="message" placeholder="Update Message" required></textarea>
        <select id="new-status">
          <option value="">No change</option>
          <option>Running</option><option>Down</option>
        </select>
        <button type="submit">Add Update</button>
      </form>
    </div>
  </div>

  <script>
    // -------- LocalStorage Helper --------
    if (!localStorage.getItem("machines")) {
      const demo = [
        {id:1,customer:"Klinik Aura",machine_name:"Lutronic Spectra XT",status:"Down",reported_date:"2023-10-01T10:00:00",pic:"Rully Candra",updates:[]},
        {id:2,customer:"RS BIH Sanur",machine_name:"Cynosure Revlite",status:"Running",reported_date:"2023-10-02T11:00:00",pic:"Muhammad Lukmansyah",updates:[]}
      ];
      localStorage.setItem("machines",JSON.stringify(demo));
    }
    const loadMachines=()=>JSON.parse(localStorage.getItem("machines")||"[]");
    const saveMachines=(m)=>localStorage.setItem("machines",JSON.stringify(m));

    // -------- Helpers --------
    const calcAging=(d)=>((new Date()-new Date(d))/(1000*60*60*24)).toFixed(1);
    const fmt=(d)=>new Date(d).toLocaleString();
    const showNotif=(msg)=>{
      const n=document.getElementById("notif");
      n.innerText=msg;n.style.display="block";
      setTimeout(()=>n.style.display="none",2000);
    };

    // -------- Render --------
    function renderKPIs(machines){
      const down=machines.filter(m=>m.status==="Down").length;
      const run=machines.filter(m=>m.status==="Running").length;
      const ages=machines.map(m=>+calcAging(m.reported_date));
      const avg=ages.length?(ages.reduce((a,b)=>a+b,0)/ages.length).toFixed(1):0;
      const max=ages.length?Math.max(...ages).toFixed(1):0;
      document.getElementById("kpis").innerHTML=`
        <div class="metric red">Down: ${down}</div>
        <div class="metric green">Running: ${run}</div>
        <div class="metric">Avg Aging: ${avg} days</div>
        <div class="metric">Oldest: ${max} days</div>`;
    }

    function renderTable(machines){
      document.getElementById("machine-table").innerHTML=machines.map(m=>`
        <tr class="${m.status==='Running'?'running':'down'}">
          <td>${m.id}</td><td>${m.customer}</td><td>${m.machine_name}</td>
          <td>${m.status}</td><td>${fmt(m.reported_date)}</td>
          <td>${calcAging(m.reported_date)}</td><td>${m.pic}</td>
        </tr>`).join("");
    }

    function renderSelect(machines){
      const opts='<option value="">Select machine</option>'+
        machines.map(m=>`<option value="${m.id}">${m.machine_name} (${m.customer})</option>`).join("");
      document.getElementById("machine-select").innerHTML=opts;
      document.getElementById("update-machine-select").innerHTML=opts;
    }

    function renderUpdates(id){
      const m=loadMachines().find(x=>x.id==id);
      document.getElementById("updates").innerHTML= !m||!m.updates.length
        ? "<p>No updates yet.</p>"
        : m.updates.map(u=>`<div><b>${u.author}</b> (${fmt(u.ts)}): ${u.message}</div>`).join("");
    }

    function renderData(){
      const m=loadMachines();
      renderKPIs(m);renderTable(m);renderSelect(m);
    }

    // -------- Events --------
    document.getElementById("machine-select").addEventListener("change",e=>renderUpdates(e.target.value));

    document.getElementById("add-machine-form").addEventListener("submit",e=>{
      e.preventDefault();
      const m=loadMachines();
      const id=(m.length?Math.max(...m.map(x=>x.id)):0)+1;
      const now=new Date().toISOString();
      m.push({
        id,customer:customer.value,machine_name:machine-name.value,status:status.value,
        reported_date:now,pic:pic.value,
        updates:[{ts:now,author:pic.value,message:init-note.value}]
      });
      saveMachines(m);renderData();e.target.reset();
      showNotif("✅ Machine added!");
    });

    document.getElementById("add-update-form").addEventListener("submit",e=>{
      e.preventDefault();
      const m=loadMachines();
      const id=update-machine-select.value;
      const x=m.find(z=>z.id==id);
      if(x){
        x.updates.push({ts:new Date().toISOString(),author:author.value,message:message.value});
        if(new-status.value) x.status=new-status.value;
        saveMachines(m);renderData();renderUpdates(id);
        e.target.reset();document.getElementById("update-machine-select").value=id;
        showNotif("✅ Update added!");
      }
    });

    // Init
    renderData();
  </script>
</body>
</html>
