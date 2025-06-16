// Detect product pages (e.g., Amazon, Walmart)
function extractBarcode() {
  // Implementation varies by website
  return document.querySelector(".barcode")?.textContent || 
         window.location.pathname.split("/")[2];
}

// Send barcode to popup
chrome.runtime.sendMessage({
  action: "barcodeScanned",
  barcode: extractBarcode()
});
