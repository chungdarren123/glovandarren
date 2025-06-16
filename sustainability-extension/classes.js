/*
"Exported" Classes:
    - product(siteName:String,productCard:documentElement)
        - Methods:
        - .scrapeInfo() -> void
        - .getInfo() -> [productName:String,productPrice:String]
        - .setIcon() -> void
    - shoppingSite(siteName:String) -> shoppingSite
        - Methods:
        - .getProducts() -> NodeList[productElement]
*/

class product {
    constructor(siteName,productCard) {
        this.siteName = siteName;
        this.cardElement = productCard;
        this.imgElement = null;
        this.nameElement = null;
        this.priceElement = null;
        this.name = null;
        this.price = null;
        this.scrapeInfo();
    }
    scrapeInfo(){
        switch(this.siteName) {
            case "amazon":
                this.nameElement = this.cardElement.querySelector('h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal');
                this.name = this.nameElement.innerText.trim();
                this.priceElement = this.cardElement.querySelector('span.a-offscreen');
                try{
                    this.price = this.priceElement.innerText.trim();
                } catch(e) {
                    this.price = "N/A"
                }
                this.imgElement = this.cardElement.querySelector('div[class="a-section aok-relative s-image-square-aspect"]');
                break;
            case "shopee":
                break;
            case "lazada":
                break;
            default:
                break;
        }
        return null
    }
    getInfo(){
        return [this.name,this.price]
    }
    setIcon(productMetrics){
        // Avoid injecting multiple times
        if(this.cardElement.querySelector(".sustainability-extension-icon")) return;
        // Setting up icon properties (analysis of product goes here)
        const icon = document.createElement("img");
        const imageUrl = chrome.runtime.getURL("./icons/icon16.png");
        icon.src = imageUrl; // sustainability icon
        icon.className = "sustainability-extension-icon";
        icon.style.width = "16px";
        icon.style.height = "16px";
        icon.style.position = "relative";
        icon.style.top = "-220px";
        icon.style.left = "-110px";
        icon.style.cursor = "pointer";
        icon.style.zIndex = "10";
        icon.title = productMetrics; // tooltip on hover

        // Add click handler to icon
        icon.addEventListener("click", () => {
            alert(productMetrics)
        })
        // Attach Icon to Product Image
        this.imgElement.appendChild(icon);
    }
}
class shoppingSite {
    constructor(siteName){
        this.siteName = siteName
    }
    getProducts(){
        var res = [];
        switch(this.siteName){
            case "amazon":
                //return document.querySelectorAll('div[role="listitem"]')
                const productElements = document.querySelectorAll('div[data-asin][data-component-type="s-search-result"]')
                productElements.forEach((productElement) => {
                    res.push(new product(this.siteName,productElement))
                })
                return res
                break;
            case "shopee":
                return null
            case "lazada":
                return null
            default:
                return null
        }
    }
}

