async function loadData() {
  const latestRes = await fetch("./data/latest.json", { cache: "no-store" });
  const historyRes = await fetch("./data/history.json", { cache: "no-store" });
  const latest = await latestRes.json();
  const history = await historyRes.json();

  const snapEl = document.querySelector(".snapshot") || document.querySelector("#snapshot");
  if (snapEl) snapEl.textContent = `Snapshot: ${latest.snapshot_date || "unavailable"}`;

  setCard("total-loc", latest.loc_total);
  setCard("test-files", latest.test_files);
  const coverage =
    latest.coverage && typeof latest.coverage === "object"
      ? latest.coverage.line_rate
      : latest.coverage;
  setCard("coverage", coverage == null ? "N/A" : `${formatPercent(coverage)}`);

  renderTrendChart("commits-chart", history.dates || [], history.commits || [], "Commits");
  renderTrendChart("loc-chart", history.dates || [], history.loc || [], "LOC");
  renderTrendChart("tests-chart", history.dates || [], history.tests || [], "Test Files");

  renderFileTypes(latest.file_types || []);
  renderEpics(latest.epics || []);
  renderTopSourceFiles(latest.source_files || []);
}

function setCard(id, value) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = value === null || value === undefined ? "--" : value;
}

function renderFileTypes(fileTypes) {
  const labels = fileTypes.map((x) => x.extension);
  const values = fileTypes.map((x) => x.files);

  const ctx = document.getElementById("chart-file-types");
  if (!ctx) return;

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: ["#59d1c9", "#f6ae2d", "#7c9cff", "#9f6fff", "#f96d9c", "#61c9f6", "#c7d36f"],
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { color: "#f4f6fb" } },
      },
    },
  });
}

function renderEpics(epics) {
  const container = document.getElementById("epics-table");
  if (!container) return;

  const rows = epics
    .map(
      (e) => `
    <tr>
      <td>${e.key}</td>
      <td>${e.commits}</td>
    </tr>
  `
    )
    .join("");

  container.innerHTML = `
    <table>
      <thead><tr><th>Epic</th><th>Commits</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

function renderTopSourceFiles(files) {
  const container = document.getElementById("top-files-table");
  if (!container) return;

  const top = files.slice(0, 10);
  const rows = top
    .map(
      (f) => `
    <tr>
      <td>${escapeHtml(f.path)}</td>
      <td>${f.loc}</td>
      <td>${f.extension}</td>
    </tr>
  `
    )
    .join("");

  container.innerHTML = `
    <table>
      <thead><tr><th>File</th><th>LOC</th><th>Type</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" }[c]));
}

loadData();

function renderTrendChart(id, labels, values, label) {
  const ctx = document.getElementById(id);
  if (!ctx) return;

  new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label,
          data: values,
          borderColor: "#59d1c9",
          backgroundColor: "rgba(89, 209, 201, 0.15)",
          tension: 0.35,
          fill: true,
          pointRadius: 2,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: { ticks: { color: "#9aa4b2" }, grid: { color: "rgba(255,255,255,0.05)" } },
        y: { ticks: { color: "#9aa4b2" }, grid: { color: "rgba(255,255,255,0.05)" } },
      },
      plugins: {
        legend: { labels: { color: "#f4f6fb" } },
      },
    },
  });
}

function formatPercent(value) {
  if (value === null || value === undefined) return "--";
  return `${(value * 100).toFixed(1)}%`;
}
