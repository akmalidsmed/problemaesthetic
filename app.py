<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aesthetic Machine Problem Monitor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            color: #333333;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            color: #2c3e50;
            font-weight: 700;
            margin-bottom: 20px;
        }
        .section {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .kpi {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        .metric {
            text-align: center;
            margin: 10px;
            background: #eaf2f8;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #d1ecf1;
        }
        .metric.red { background: #f8d7da; border-color: #f5c6cb; }
        .metric.green { background: #d4edda; border-color: #c3e6cb; }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #2980b9;
            color: white;
        }
        .down {
            background-color: #f8d7da;
        }
        .running {
            background-color: #d4edda;
        }
        .chat-msg {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
            background: #f8f9fa;
        }
        .chat-author {
            font-weight: bold;
            color: #2980b9;
        }
        .chat-time {
            font-size: small;
            color: #7f8c8d;
        }
        input, select, textarea {
            width: 100%;
            padding: 8px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            background: #eaf2f8;
        }
        button {
            background: #2980b9;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
        }
        button:hover {
            background: #3498db;
        }
        .form-section {
            max-width: 600px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🛠️ Aesthetic Machine Problem Monitor</h1>

        <div class="section">
            <h2>KPIs</h2>
            <div class="kpi" id="kpis"></div>
        </div>

        <div class="section">
            <h2>Machine Problems</h2>
            <table id="machine-table"></table>
        </div>

        <div class="section">
            <h2>Problem Updates</h2>
            <select id="machine-select"></select>
            <div id="updates"></div>
        </div>

        <div class="section form-section">
            <h2>Add New Machine</h2>
            <form id="add-machine-form">
                <input type="text" id="customer" placeholder="Customer" required>
                <input type="text" id="machine-name" placeholder="Machine Name" required>
                <select id="status">
                    <option value="Down">Down</option>
                    <option value="Running">Running</option>
                </select>
                <input type="text" id="pic" placeholder="PIC" required>
                <textarea id="init-note" placeholder="Initial Problem Note" required></textarea>
                <button type="submit">Create</button>
            </form>
        </div>

        <div class="section form-section">
            <h2>Add Update</h2>
            <form id="add-update-form">
                <select id="update-machine-select"></select>
                <input type="text" id="author" placeholder="Your Name" required>
                <textarea id="message" placeholder="Update Message" required></textarea>
                <select id="new-status">
                    <option value="">No change</option>
                    <option value="Running">Running</option>
                    <option value="Down">Down</option>
                </select>
                <button type="submit">Add Update</button>
            </form>
        </div>
    </div>

    <script>
        // Sample data (simulates DB)
        if (!localStorage.getItem('machines')) {
            const machines = [
                { id: 1, customer: 'Klinik Aura', machine_name: 'Lutronic Spectra XT', status: 'Down', reported_date: '2023-10-01T10:00:00', pic: 'Rully Candra', updates: [] },
                { id: 2, customer: 'RS BIH Sanur', machine_name: 'Cynosure Revlite', status: 'Running', reported_date: '2023-10-02T11:00:00', pic: 'Muhammad Lukmansyah', updates: [] },
                { id: 3, customer: 'Klinik Everglow', machine_name: 'Lumenis M22', status: 'Down', reported_date: '2023-10-03T12:00:00', pic: 'Denny Firmansyah', updates: [] },
            ];
            localStorage.setItem('machines', JSON.stringify(machines));
        }

        function loadMachines() {
            return JSON.parse(localStorage.getItem('machines') || '[]');
        }

        function saveMachines(machines) {
            localStorage.setItem('machines', JSON.stringify(machines));
        }

        function calcAgingDays(reportedDate) {
            const now = new Date();
            const reported = new Date(reportedDate);
            const diff = now - reported;
            return (diff / (1000 * 60 * 60 * 24)).toFixed(1);
        }

        function humanTs(ts) {
            const date = new Date(ts);
            return date.toLocaleString();
        }

        function renderKPIs(machines) {
            const totalDown = machines.filter(m => m.status === 'Down').length;
            const totalRunning = machines.filter(m => m.status === 'Running').length;
            const agingDays = machines.map(m => parseFloat(calcAgingDays(m.reported_date)));
            const avgAging = agingDays.length ? (agingDays.reduce((a, b) => a + b, 0) / agingDays.length).toFixed(1) : 0;
            const oldest = agingDays.length ? Math.max(...agingDays).toFixed(1) : 0;
            
            const kpis = `
                <div class='metric red'>Total Down: ${totalDown}</div>
                <div class='metric green'>Total Running: ${totalRunning}</div>
                <div class='metric'>Avg Aging (days): ${avgAging}</div>
                <div class='metric'>Oldest Case (days): ${oldest}</div>
            `;
            document.getElementById('kpis').innerHTML = kpis;
        }

        function renderTable(machines) {
            let html = `
                <tr>
                    <th>ID</th>
                    <th>Customer</th>
                    <th>Machine Name</th>
                    <th>Status</th>
                    <th>Reported Date</th>
                    <th>Aging Days</th>
                    <th>PIC</th>
                </tr>
            `;
            machines.forEach(m => {
                const aging = calcAgingDays(m.reported_date);
                const classStatus = m.status === 'Running' ? 'running' : 'down';
                html += `
                    <tr class='${classStatus}'>
                        <td>${m.id}</td>
                        <td>${m.customer}</td>
                        <td>${m.machine_name}</td>
                        <td>${m.status}</td>
                        <td>${humanTs(m.reported_date)}</td>
                        <td>${aging}</td>
                        <td>${m.pic}</td>
                    </tr>
                `;
            });
            document.getElementById('machine-table').innerHTML = html;
        }

        function renderSelect(machines) {
            let html = '<option value="">Select machine</option>';
            machines.forEach(m => {
                html += `<option value="${m.id}">${m.machine_name} (${m.customer})</option>`;
            });
            document.getElementById('machine-select').innerHTML = html;
            document.getElementById('update-machine-select').innerHTML = html;
        }

        function renderUpdates(machineId) {
            const machines = loadMachines();
            const machine = machines.find(m => m.id == machineId);
            let html = '';
            if (!machine || !machine.updates.length) {
                html = '<p>No updates yet.</p>';
            } else {
                machine.updates.forEach(u => {
                    html += `
                        <div class="chat-msg">
                            <span class="chat-author">${u.author}</span>
                            <span class="chat-time">(${humanTs(u.ts)})</span>: ${u.message}
                        </div>
                    `;
                });
            }
            document.getElementById('updates').innerHTML = html;
        }

        // Event listeners
        document.getElementById('machine-select').addEventListener('change', (e) => {
            renderUpdates(e.target.value);
        });

        document.getElementById('add-machine-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const machines = loadMachines();
            const newId = Math.max(...machines.map(m => m.id), 0) + 1;
            const now = new Date().toISOString();
            const newMachine = {
                id: newId,
                customer: document.getElementById('customer').value,
                machine_name: document.getElementById('machine-name').value,
                status: document.getElementById('status').value,
                reported_date: now,
                pic: document.getElementById('pic').value,
                updates: [{
                    ts: now,
                    author: document.getElementById('pic').value,
                    message: document.getElementById('init-note').value
                }]
            };
            machines.push(newMachine);
            saveMachines(machines);
            renderData();
            e.target.reset();
            alert('Machine added!');
        });

        document.getElementById('add-update-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const machines = loadMachines();
            const machineId = document.getElementById('update-machine-select').value;
            const machine = machines.find(m => m.id == machineId);
            if (machine) {
                const now = new Date().toISOString();
                const update = {
                    ts: now,
                    author: document.getElementById('author').value,
                    message: document.getElementById('message').value
                };
                machine.updates.push(update);
                const newStatus = document.getElementById('new-status').value;
                if (newStatus) {
                    machine.status = newStatus;
                }
                saveMachines(machines);
                renderData();
                renderUpdates(machineId);
                e.target.reset();
                alert('Update added!');
            }
        });

        function renderData() {
            const machines = loadMachines();
            renderKPIs(machines);
            renderTable(machines);
            renderSelect(machines);
        }

        // Initial render
        renderData();
    </script>
</body>
</html>
</content>
</create_file>
