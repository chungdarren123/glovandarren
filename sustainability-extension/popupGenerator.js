/*
"Exported" functions
- showModalPopup(htmlContent)
"Exported" constants
- analyticsHtml
*/

function showModalPopup(htmlContent) {
  // Create overlay
  const overlay = document.createElement("div");
  overlay.className = "popup-overlay";

  // Create popup
  const popup = document.createElement("div");
  popup.className = "popup-box";
  popup.innerHTML = htmlContent;

  // Close popup on outside click
  overlay.addEventListener("click", () => {
    document.body.removeChild(overlay);
  });

  // Prevent popup click from closing
  popup.addEventListener("click", (e) => e.stopPropagation());

  // Add popup to overlay, and overlay to body
  overlay.appendChild(popup);
  document.body.appendChild(overlay);
}

const analyticsHtml = `



`
