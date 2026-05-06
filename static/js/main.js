document.addEventListener("submit", (event) => {
  const button = event.target.querySelector("button[type='submit'], button:not([type])");
  if (button) {
    button.dataset.originalText = button.textContent;
    button.textContent = "Please wait...";
    button.disabled = true;
  }
});

setTimeout(() => {
  document.querySelectorAll(".toast-stack .alert").forEach((alert) => alert.remove());
}, 4500);
