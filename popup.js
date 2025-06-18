async function fetchESGData(barcode) {
  const response = await fetch(
    `http://localhost:8000/products/search/?q=${barcode}`
  );
  const products = await response.json();
  
  if (products.length > 0) {
    const scoreResponse = await fetch(
      `http://localhost:8000/products/${products[0].id}/latest-score`
    );
    return await scoreResponse.json();
  }
  return null;
}

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "barcodeScanned") {
    fetchESGData(request.barcode).then(score => {
      document.getElementById("score").textContent = 
        score ? `Overall: ${score.overall_score}/100` : "No ESG data";
      
      if (score) {
        document.getElementById("breakdown").innerHTML = `
          <p>🌿 Environmental: ${score.environmental_score}/100</p>
          <p>👥 Social: ${score.social_score}/100</p>
          <p>🏛 Governance: ${score.governance_score}/100</p>
          <p>💰 Economic: ${score.economic_score}/100</p>
        `;
      }
    });
  }
});
