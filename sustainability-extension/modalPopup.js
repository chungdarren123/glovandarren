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



function animateProgressBar(progressEndValue) {
    let progressStartValue = 0;
    let speed = 20;
    let progressInterval;

    const circularProgress = document.querySelector('.circular-progress');
    const progressValue = document.querySelector('.progress-value');

    clearInterval(progressInterval);
    progressStartValue = 0;

    progressInterval = setInterval(() => {
        if (progressStartValue >= progressEndValue) {
            clearInterval(progressInterval);
        } else {
            progressStartValue++;
            updateProgress(progressStartValue);
        }
    }, speed);

    // Function to update the progress display
    function updateProgress(value) {
        // Update the progress text
        progressValue.textContent = `${value}/100`;

        // Update the conic-gradient
        circularProgress.style.background = `conic-gradient(#2e6f40 ${value * 3.6}deg, #e0e0e0 0deg)`;
    }
}

const analyticsHtml = `
<div class="analysis-details-container">
    <div class="circular-progress">
        <div class="progress-value">Loading...</div>
    </div>
    <div class="analysis-details">
        <div class="analysis-name">Name: Loading...</div>
        <div class="analysis-price">Price: Loading...</div>
        <div class="analysis-analysis">Analysis: Loading...</div>
    </div>
</div>

`
/*
const analyticsHtml = `
<div class="container">
    <div class="circular-progress">
        <div class="progress-value">Loading...</div>
    </div>

    <div class="controls">
        <button id="start-btn">Start Progress</button>
        <input type="range" id="progress-slider" min="0" max="100" value="0">
    </div>
</div>
`
*/
