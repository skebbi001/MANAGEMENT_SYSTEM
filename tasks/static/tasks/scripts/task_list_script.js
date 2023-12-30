document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(
    ".show-details-btn, .delete-task-btn, .create-task-btn"
  );

  const csrfToken = document.querySelector("meta[name='csrf-token']").content;

  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      if (button.classList.contains("create-task-btn")) {
        window.location.href = "{% url 'create_task' %}";
      } else {
        const taskId = this.getAttribute("data-task-id");
        const detailsContainer = document.getElementById(
          `details-container-${taskId}`
        );

        if (button.classList.contains("delete-task-btn")) {
          // If it's a delete button, send a DELETE request to the server
          fetch(`/tasks/${taskId}/delete/`, {
            method: "DELETE",
          }).then(() => {
            // Redirect or update the UI as needed
            window.location.reload(); // Example: Refresh the page
          });
        } else {
          // Toggle visibility of task details
          if (detailsContainer.innerHTML.trim() === "") {
            // Fetch and display task details
            fetch(`/tasks/${taskId}/`)
              .then((response) => response.text())
              .then((data) => {
                detailsContainer.innerHTML = data;
                button.classList.remove("show-details-btn");
                button.classList.add("hide-details-btn");
                button.innerText = "Hide Details";
              });
          } else {
            detailsContainer.innerHTML = ""; // Clear content
            button.classList.remove("hide-details-btn");
            button.classList.add("show-details-btn");
            button.innerText = "Show Details";
          }
        }
      }
    });
  });
});
