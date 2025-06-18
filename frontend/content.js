// Listen for clicks on product links
document.addEventListener('click', async (event) => {
  let target = event.target;
  
  // Traverse up the DOM to find product link
  while (target && !target.href && target.parentNode) {
    target = target.parentNode;
  }
  
  if (target && target.href && target.href.includes('/dp/')) {
    event.preventDefault();
    event.stopPropagation();
    
    // Get product details
    const productUrl = target.href;
    const productName = target.innerText.trim();
    
    // Send to background for processing
    chrome.runtime.sendMessage({
      type: 'PRODUCT_CLICK',
      data: {
        url: productUrl,
        name: productName
      }
    });
  }
});

// Listen for messages from popup/background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'SHOW_RECOMMENDATION') {
    showRecommendationBubble(message.data);
  }
});

function showRecommendationBubble(data) {
  // Create and position the recommendation bubble
  const bubble = document.createElement('div');
  bubble.className = 'nutrition-bubble';
  bubble.innerHTML = `
    <h4>Healthier Alternative Found</h4>
    <p>Current: ${data.currentScore} | Alternative: ${data.betterScore}</p>
    <button id="view-details">View Details</button>
  `;
  
  document.body.appendChild(bubble);
  
  // Position near the clicked element
  // Add styling and event handlers
}
