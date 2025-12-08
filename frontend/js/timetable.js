const BASE_URL = "http://127.0.0.1:5000";

function addExam() {
  const subject = document.getElementById("subject").value;
  const examDate = document.getElementById("examDate").value;
  const totalChapters = Number(document.getElementById("totalChapters").value);
  const hoursPerDay = Number(document.getElementById("hoursPerDay").value);

  fetch(`${BASE_URL}/api/exams`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      subject,
      examDate,
      totalChapters,
      hoursPerDay,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("Exam saved:", data);
      alert("Exam saved with ID: " + data.examId);
      document.getElementById("examId").value = data.examId;
    })
    .catch((err) => {
      console.error(err);
      alert("Error saving exam");
    });
}

function generateTimetable() {
  const examId = Number(document.getElementById("examId").value);

  fetch(`${BASE_URL}/api/generate-timetable`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ examId }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("Timetable generated:", data);
      if (!data.timetable) {
        alert("No timetable in response");
        return;
      }
      renderTimetable(data.timetable);
    })
    .catch((err) => {
      console.error(err);
      alert("Error generating timetable");
    });
}

function renderTimetable(rows) {
  const tbody = document.getElementById("timetableBody");
  tbody.innerHTML = "";

  rows.forEach((row) => {
    const tr = document.createElement("tr");

    const tdDate = document.createElement("td");
    tdDate.textContent = row.date;

    const tdStart = document.createElement("td");
    tdStart.textContent = row.start_chapter ?? row.startChapter;

    const tdEnd = document.createElement("td");
    tdEnd.textContent = row.end_chapter ?? row.endChapter;

    const tdHours = document.createElement("td");
    tdHours.textContent = row.hours;

    tr.appendChild(tdDate);
    tr.appendChild(tdStart);
    tr.appendChild(tdEnd);
    tr.appendChild(tdHours);

    tbody.appendChild(tr);
  });
}
