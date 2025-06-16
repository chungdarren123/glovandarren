console.log("This script runs on every page.");

//const amazonElementId = 'span[data-component-type="s-product-image"]';
const amazonSite = new shoppingSite("amazon");
const shopeeSite = new shoppingSite("shopee");
const lazadaSite = new shoppingSite("lazada");

window.addEventListener("load", () => {
  setTimeout(addIconsToSite(amazonSite), 1000); // give time for page to load
});

