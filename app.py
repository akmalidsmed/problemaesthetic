import streamlit as st
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="Machine Problem Monitor - Popup Detail", layout="wide")

HTML = r"""<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Machine Problem Monitor - Popup Detail</title>
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
      font-size: 2.5rem;
      text-align: center;
      margin-bottom: 30px;
      color: #1e40af;
      text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
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
    }
    .summary-item.total-problem {
      background: linear-gradient(45deg, #64748b, #475569);
      box-shadow: 0 6px 15px rgba(71, 85, 105, 0.7);
    }
    .summary-item.red {
      background: linear-gradient(45deg, #dc2626, #b91c1c);
      box-shadow: 0 6px 15px rgba(185, 28, 28, 0.7);
    }
    .summary-item.green {
      background: linear-gradient(45deg, #059669, #10b981);
      box-shadow: 0 6px 15px rgba(16, 185, 129, 0.5);
    }
    .summary-item:hover {
      transform: scale(1.05);
    }
    .summary-label {
      font-size: 1rem;
      opacity: 0.8;
      margin-bottom: 8px;
    }
    .summary-value {
      font-size: 2.5rem;
      line-height: 1;
    }

    /* Scrollable table wrapper */
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
    th {
      background: #3b82f6;
      color: white;
      border-radius: 12px;
      user-select: none;
    }
    tr {
      background: #f1f5f9;
      box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
      border-radius: 12px;
      transition: background-color 0.3s ease;
    }
    tr:hover {
      background-color: #bfdbfe;
    }
    .status-badge {
      display: inline-block;
      padding: 4px 12px;
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
    .detail-btn:hover,
    .detail-btn:focus {
      color: #1e40af;
      outline: none;
    }

    /* Modal styles */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.5);
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
      border-radius: 15px;
      max-width: 600px;
      width: 90%;
      max-height: 80vh;
      overflow-y: auto;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
      padding: 25px 30px;
      position: relative;
    }
    .modal h2 {
      color: #1e40af;
      font-weight: 900;
      margin-bottom: 20px;
      font-size: 1.8rem;
    }
    .modal .detail-row {
      margin-bottom: 12px;
      font-size: 1.1rem;
      color: #1e293b;
    }
    .modal .detail-label {
      font-weight: 700;
      color: #2563eb;
    }
    .modal .updates {
      margin-top: 20px;
      border-top: 2px solid #93c5fd;
      padding-top: 15px;
    }
    .modal .update-item {
      background: #dbeafe;
      border-radius: 10px;
      padding: 10px 15px;
      margin-bottom: 12px;
      box-shadow: inset 0 0 6px rgba(59, 130, 246, 0.3);
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
      top: 15px;
      right: 15px;
      background: transparent;
      border: none;
      font-size: 1.5rem;
      font-weight: 700;
      color: #2563eb;
      cursor: pointer;
      transition: color 0.2s ease;
    }
    .modal-close-btn:hover {
      color: #1e40af;
    }

    @media (max-width: 640px) {
      .summary {
        flex-direction: column;
        align-items: center;
      }
      .summary-item {
        width: 80%;
        height: 140px;
        margin-bottom: 15px;
      }
      .summary-value {
        font-size: 2rem;
      }
      .table-wrapper {
        padding: 5px;
      }
      th, td {
        font-size: 0.9rem;
        padding: 8px 10px;
      }
      .modal {
        max-width: 95%;
        padding: 20px;
      }
      .modal h2 {
        font-size: 1.5rem;
      }
      .modal .detail-row {
        font-size: 1rem;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🛠️ Machine Problem Monitor</h1>

    <!-- Summary KPIs -->
    <div class="summary" id="summary"></div>

    <!-- Scrollable Table Wrapper -->
    <div class="table-wrapper" aria-label="List of machines with problems">
      <table id="machine-table"></table>
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

<script>
  if (!localStorage.getItem('machines')) {
    const machines = [
      { id: 1, customer: 'Klinik Aura', machine_name: 'Lutronic Spectra XT', status: 'Down', reported_date: '2023-10-01T10:00:00', pic: 'Rully Candra', updates: [
        { ts: '2023-10-02T09:00:00', author: 'Rully Candra', message: 'Initial report: machine not powering on.' },
        { ts: '2023-10-03T14:30:00', author: 'Technician A', message: 'Checked power supply, replaced fuse.' }
      ] },
      { id: 2, customer: 'RS BIH Sanur', machine_name: 'Cynosure Revlite', status: 'Running', reported_date: '2023-10-02T11:00:00', pic: 'Muhammad Lukmansyah', updates: [] },
      { id: 3, customer: 'Klinik Everglow', machine_name: 'Lumenis M22', status: 'Down', reported_date: '2023-10-03T12:00:00', pic: 'Denny Firmansyah', updates: [
        { ts: '2023-10-04T08:00:00', author: 'Denny Firmansyah', message: 'Laser calibration error detected.' }
      ] },
    ];
    localStorage.setItem('machines', JSON.stringify(machines));
  }

  function loadMachines() {
    return JSON.parse(localStorage.getItem('machines') || '[]');
  }

  function formatDateOnly(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, { year: 'numeric', month: '2-digit', day: '2-digit' });
  }

  function calcAgingDays(reportedDate) {
    const now = new Date();
    const reported = new Date(reportedDate);
    const diff = now - reported;
    return Math.floor(diff / (1000 * 60 * 60 * 24));
  }

  function humanTs(ts) {
    const date = new Date(ts);
    return date.toLocaleString();
  }

  function renderSummary(machines) {
    const totalDown = machines.filter(m => m.status === 'Down').length;
    const totalRunning = machines.filter(m => m.status === 'Running').length;
    const totalProblem = totalDown + totalRunning;

    const summaryHTML = `
      <div class="summary-item total-problem">
        <div class="summary-label">Total Problem</div>
        <div class="summary-value">${totalProblem}</div>
      </div>
      <div class="summary-item red">
        <div class="summary-label">Total Down</div>
        <div class="summary-value">${totalDown}</div>
      </div>
      <div class="summary-item green">
        <div class="summary-label">Total Running</div>
        <div class="summary-value">${totalRunning}</div>
      </div>
    `;
    document.getElementById('summary').innerHTML = summaryHTML;
  }

  function renderMachineTable(machines) {
    const problemMachines = machines.filter(m => m.status === 'Down');

    if (problemMachines.length === 0) {
      document.getElementById('machine-table').innerHTML = '<tr><td colspan="7" class="text-center font-semibold p-6">No machines currently down.</td></tr>';
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
      if (m.updates.length > 0) {
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
          <td>${lastUpdate}</td>
          <td><button class="detail-btn" data-id="${m.id}" aria-label="View details for machine ${m.machine_name}">Detail</button></td>
        </tr>
      `;
    });

    document.getElementById('machine-table').innerHTML = html;

    // Pasang event listener hanya pada tombol detail
    document.querySelectorAll('.detail-btn').forEach(btn => {
      btn.addEventListener('click', () => openModal(btn.dataset.id));
    });
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
    if (machine.updates.length === 0) {
      updatesHTML = '<p>No updates yet.</p>';
    } else {
      updatesHTML = machine.updates.slice().reverse().map(u => `
        <div class="update-item">
          <span class="update-author">${u.author}</span>
          <span class="update-time">(${humanTs(u.ts)})</span>: ${u.message}
        </div>
      `).join('');
    }

    modalContent.innerHTML = `
      <div class="detail-row"><span class="detail-label">ID:</span> ${machine.id}</div>
      <div class="detail-row"><span class="detail-label">Customer:</span> ${machine.customer}</div>
      <div class="detail-row"><span class="detail-label">Unit:</span> ${machine.machine_name}</div>
      <div class="detail-row"><span class="detail-label">Status:</span> ${machine.status}</div>
      <div class="detail-row"><span class="detail-label">Reported Date:</span> ${formatDateOnly(machine.reported_date)}</div>
      <div class="detail-row"><span class="detail-label">Aging (days):</span> ${aging}</div>
      <div class="detail-row"><span class="detail-label">PIC:</span> ${machine.pic}</div>
      <div class="updates">
        <h3 class="detail-label mb-2">Updates:</h3>
        ${updatesHTML}
      </div>
    `;

    modalOverlay.classList.add('active');
    modalOverlay.focus();
  }

  function closeModal() {
    modalOverlay.classList.remove('active');
  }

  modalCloseBtn.addEventListener('click', closeModal);

  modalOverlay.addEventListener('click', e => {
    if (e.target === modalOverlay) {
      closeModal();
    }
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
      closeModal();
    }
  });

  function render() {
    const machines = loadMachines();
    renderSummary(machines);
    renderMachineTable(machines);
  }

  render();
</script>
</body>
</html>
"""

st.markdown("# 🛠️ Machine Problem Monitor", help="Embedded HTML app below")
st_html(HTML, height=1100, scrolling=True)
