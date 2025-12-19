document.getElementById("saveExamBtn").addEventListener("click", async () => {
  const subject = document.getElementById("subject").value;
  const examDate = document.getElementById("examDate").value;
  const totalChapters = document.getElementById("totalChapters").value;
  const hoursPerDay = document.getElementById("hoursPerDay").value;

  console.log("Sending exam data...");

  const response = await fetch("http://127.0.0.1:5000/save-exam", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      subject,
      exam_date: examDate,
      total_chapters: totalChapters,
      hours_per_day: hoursPerDay
    })
  });

  const data = await response.json();
  alert(data.message);
});
