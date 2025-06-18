document.addEventListener('DOMContentLoaded', () => {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, {type: 'GET_CURRENT_PRODUCT'}, (response) => {
      if (response) {
        updateUI(response);
      }
    });
  });
  
  document.getElementById('options-button').addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });
});

function updateUI(data) {
  const currentScores = document.getElementById('current-scores');
  currentScores.innerHTML = `
    <p>Nutri-Score: ${data.currentProduct.nutriScore}</p>
    <p>NOVA Score: ${data.currentProduct.novaScore}</p>
    <p>Eco-Score: ${data.currentProduct.ecoScore}</p>
    <p>Total: ${data.currentProduct.total.toFixed(1)}</p>
  `;
  
  const recList = document.getElementById('recommendations-list');
  recList.innerHTML = data.betterAlternatives.slice(0, 3).map(alt => `
    <div class="recommendation">
      <h4>${alt.product.product_name}</h4>
      <p>Nutri: ${alt.scores.nutriScore} | NOVA: ${alt.scores.novaScore} | Eco: ${alt.scores.ecoScore}</p>
      <p>Total Score: ${alt.scores.total.toFixed(1)}</p>
    </div>
  `).join('');
}
