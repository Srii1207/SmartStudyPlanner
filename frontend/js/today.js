const BASE_URL = "http://127.0.0.1:5000";

async function loadTodayTasks() {
  try {
    const response = await fetch(`${BASE_URL}/api/today`);
    const data = await response.json();

    const list = document.getElementById("today-list");
    list.innerHTML = "";

    (data.tasks || []).forEach((task) => {
      const li = document.createElement("li");

      li.textContent = `${task.start_time || ""} ${task.subject || ""} - ${
        task.description || ""
      }`;

      list.appendChild(li);
    });
  } catch (err) {
    console.error("Error loading today's tasks:", err);
  }
}

async function handleAddTask(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);

  const payload = {
    subject: formData.get("subject"),
    date: formData.get("date"),
    start_time: formData.get("start_time"),
    end_time: formData.get("end_time"),
    description: formData.get("description"),
  };

  try {
    const response = await fetch(`${BASE_URL}/api/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    console.log("Add task response:", data);

    form.reset();
    await loadTodayTasks(); // refresh list
  } catch (err) {
    console.error("Error adding task:", err);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadTodayTasks();

  const form = document.getElementById("add-task-form");
  if (form) {
    form.addEventListener("submit", handleAddTask);
  }
});
