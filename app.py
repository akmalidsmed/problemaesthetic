<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Aesthetic Machine Monitor</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background: linear-gradient(135deg,#f5f7fa,#e6eef9); }
    .card { background: rgba(255,255,255,0.9); box-shadow: 0 6px 18px rgba(36,37,38,0.08); border-radius: 12px; }
    .bubble { max-width: 78%; padding: 10px 14px; border-radius: 16px; display: inline-block; line-height: 1.3; }
    .bubble.me { background: #daf1ff; border-bottom-right-radius: 6px; }
    .bubble.other { background: #f1f5f9; border-bottom-left-radius: 6px; }
    .meta { font-size: 12px; color: #6b7280; margin-top: 4px; }
    .fade-in { animation: fadeIn .28s ease; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
    .kpi { min-width: 140px; }
    @media (max-width: 900px) {
      .layout-grid { grid-template-columns: 1fr; }
      .chat-pane { max-height: 340px; }
    }
  </style>
</head>
<body class="min-h-screen antialiased text-slate-800">
  <div class="max-w-7xl mx-auto p-6">
    <header class="mb-6">
      <h1 class="text-2xl md:text-3xl font-semibold">Aesthetic Machine Monitor</h1>
    </header>

    <main class="grid layout-grid grid-cols-3 gap-6">
      <section class="col-span-2 space-y-4">
        <div class="card p-4 flex flex-wrap gap-3 items-center">
          <div id="kpi-down" class="kpi p-3 rounded-lg bg-rose-50 border border-rose-100">
            <div class="text-sm text-rose-600">Down</div>
            <div id="kpi-down-val" class="text-2xl font-bold">0</div>
          </div>
          <div id="kpi-running" class="kpi p-3 rounded-lg bg-emerald-50 border border-emerald-100">
            <div class="text-sm text-emerald-600">Running</div>
            <div id="kpi-running-val" class="text-2xl font-bold">0</div>
          </div>
          <div class="kpi p-3 rounded-lg bg-slate-50 border border-slate-100">
            <div class="text-sm text-slate-600">Avg Aging (days)</div>
            <div id="kpi-avg" class="text-2xl font-bold">0</div>
          </div>
          <div class="kpi p-3 rounded-lg bg-slate-50 border border-slate-100">
            <div class="text-sm text-slate-600">Oldest Case (days)</div>
            <div id="kpi-oldest" class="text-2xl font-bold">0</div>
          </div>

          <div class="ml-auto flex gap-2">
            <button id="btn-export" class="px-3 py-2 rounded-md bg-indigo-600 text-white text-sm">Export CSV</button>
            <button id="btn-reset" class="px-3 py-2 rounded-md bg-rose-50 text-rose-700 border border-rose-100 text-sm">Reset Demo</button>
          </div>
        </div>

        <div class="card p-4">
          <h2 class="font-medium mb-3">Machines</h2>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="text-left text-slate-600">
                  <th class="p-2">ID</th>
                  <th class="p-2">Customer</th>
                  <th class="p-2">Machine</th>
                  <th class="p-2">Status</th>
                  <th class="p-2">Reported</th>
                  <th class="p-2">Aging (days)</th>
                  <th class="p-2">PIC</th>
                </tr>
              </thead>
              <tbody id="machine-table" class="divide-y"></tbody>
            </table>
          </div>
        </div>

        <div class="card p-4 grid md:grid-cols-2 gap-4">
          <div>
            <h3 class="font-medium mb-2">Add New Machine</h3>
            <!-- Form fields will go here -->
          </div>
          <div>
            <h3 class="font-medium mb-2">Add Update</h3>
            <!-- Form fields will go here -->
          </div>
        </div>
      </section>

      <aside class="card p-4 chat-pane overflow-y-auto">
        <h3 class="font-medium mb-2">Machine Updates</h3>
        <div id="chat-box" class="space-y-3"></div>
      </aside>
    </main>
  </div>
</body>
</html>
