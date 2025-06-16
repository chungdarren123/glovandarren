document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("click-me");

  // ✅ Check if listener has already been added (safeguard)
  if (!button.hasAttribute("data-click-bound")) {
    button.setAttribute("data-click-bound", "true");

    button.addEventListener("click", () => {
      alert("Button clicked!");
    });
  }
});

