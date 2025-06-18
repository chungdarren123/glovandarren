/*
"Exported" Functions:
    - addIconsToSite(siteObject:shoppingSite) -> void
    -
*/
function downloadAsJSON(data, filename = "products.json") {
  const jsonStr = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonStr], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function analyse(productObj){

}

function addIconsToSite(siteObject) {
    var products = siteObject.getProducts();
    if (!products) return;
    products.forEach((product) => {
        // Get Product Information
        // console.log(product.getInfo());

        // Run Analysis of Product
        // analysis(productInfo)
        // productMetrics="sustainability metrics go here"

        // Generate & Attach Icon Based on Analysis of product
        //icon = siteObject.attachIcon(product, productMetrics);
        //product.setIcon(productMetrics);
    });
}


