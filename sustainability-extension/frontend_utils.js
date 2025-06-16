/*
"Exported" Functions:
    - addIconsToSite(siteObject:shoppingSite) -> void
    -
*/


function addIconsToSite(siteObject) {
    var products = siteObject.getProducts();
    products.forEach((product) => {
        // Avoid injecting multiple times
        // if (product.querySelector(".sustainability-extension-icon")) return;

        // Get Product Information
        console.log(product.getInfo());

        // Run Analysis of Product
        // analysis(productInfo)
        productMetrics="sustainability metrics go here"

        // Generate & Attach Icon Based on Analysis of product
        //icon = siteObject.attachIcon(product, productMetrics);
        product.setIcon(productMetrics);
    });
}
