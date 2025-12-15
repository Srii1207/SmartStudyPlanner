// URL of your backend. If backend and frontend run on same PC:
// Flask default = http://127.0.0.1:5000
const BASE_URL = "http://127.0.0.1:5000";

async function loadTimetable() {
  try {
    const response = await fetch(`${BASE_URL}/api/timetable`);
    const data = await response.json();

    const tbody = document.getElementById("timetable-body");
    tbody.innerHTML = ""; // clear existing rows

    (data.timetable || []).forEach((row) => {
      const tr = document.createElement("tr");

      const dateTd = document.createElement("td");
      dateTd.textContent = row.task_date || ""; // from DB

      const subjectTd = document.createElement("td");
      subjectTd.textContent = row.subject || "";

      const startTd = document.createElement("td");
      startTd.textContent = row.start_time || "";

      const endTd = document.createElement("td");
      endTd.textContent = row.end_time || "";

      const descTd = document.createElement("td");
      descTd.textContent = row.description || "";

      tr.appendChild(dateTd);
      tr.appendChild(subjectTd);
      tr.appendChild(startTd);
      tr.appendChild(endTd);
      tr.appendChild(descTd);

      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Error loading timetable:", err);
  }
}

// Call on page load
document.addEventListener("DOMContentLoaded", loadTimetable);
