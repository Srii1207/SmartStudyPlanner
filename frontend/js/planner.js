const form = document.getElementById("plannerForm");
const taskInput = document.getElementById("task");
const taskList = document.getElementById("taskList");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const task = taskInput.value;

  try {
    const response = await fetch("http://127.0.0.1:5000/add-task", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ task })
    });

    const data = await response.json();

    if (response.ok) {
      const li = document.createElement("li");
      li.textContent = data.task;
      taskList.appendChild(li);
      taskInput.value = "";
    } else {
      alert(data.message);
    }

  } catch (error) {
    console.error("Error:", error);
    alert("Backend not running");
  }
});
