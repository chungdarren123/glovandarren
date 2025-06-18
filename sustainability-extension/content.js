console.log("This script runs on every page.");

//const amazonElementId = 'span[data-component-type="s-product-image"]';
const shoppingSite = new SiteObj(window.location.hostname,window.location.href);

if (shoppingSite.getSiteName() != "") {
    window.addEventListener("load", () => {
        setTimeout(addIconsToSite(shoppingSite), 1000); // give time for page to load
    });
}
