const API_BASE = (() => {
  const isLocalHost =
    window.location.hostname === "127.0.0.1" ||
    window.location.hostname === "localhost";
  if (isLocalHost && window.location.port !== "8000") {
    // Local static frontend + local FastAPI backend
    return "http://127.0.0.1:8000";
  }
  // Vercel (same origin) or backend served on same port
  return "";
})();

async function postJSON(path, payload) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const income = Number(document.getElementById("income").value || 0);
  const expenses = Number(document.getElementById("expenses").value || 0);
  const savings = Number(document.getElementById("savings").value || 0);
  const out = document.getElementById("analysisOut");
  try {
    const data = await postJSON("/analyze", { income, expenses, savings });
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
});

document.getElementById("csvBtn").addEventListener("click", async () => {
  const file = document.getElementById("csvFile").files[0];
  const out = document.getElementById("csvOut");
  if (!file) {
    out.textContent = "Please select a CSV file.";
    return;
  }
  const form = new FormData();
  form.append("file", file);
  try {
    const res = await fetch(`${API_BASE}/expense/analyze-csv`, {
      method: "POST",
      body: form,
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
});

document.getElementById("chatBtn").addEventListener("click", async () => {
  const message = document.getElementById("chatMsg").value.trim();
  const out = document.getElementById("chatOut");
  if (!message) {
    out.textContent = "Please type a question.";
    return;
  }
  const income = Number(document.getElementById("income").value || 0);
  const expenses = Number(document.getElementById("expenses").value || 0);
  try {
    const data = await postJSON("/chat", {
      message,
      income,
      expenses,
      risk_profile: "Moderate",
      goals: ["Emergency Fund"],
    });
    out.textContent = data.reply;
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
});
