/*
"Exported" Classes:
    - ProductObj(siteName:String,productCard:documentElement)
        - Methods:
        - .scrapeInfo() -> void
        - .getInfo() -> [productName:String,productPrice:String]
        - .setIcon() -> void
    - SiteObj(siteName:String)
        - Methods:
        - .getProducts() -> [product:ProductObj,...]
*/

class ProductObj {
    constructor(name,price,icon) {
        //this.imgElement = imgElement;
        this.icon = icon;
        this.name = name;
        this.price = price;
        this.analysis = null;
    }
    getInfo(){
        return [this.name,this.price]
    }
    async getAnalysis(){

    }
    async updateIcon(){

    }
}
class SiteObj {
    constructor(hostname){
        this.hostname = hostname;
        this.siteName = "";
        this.getSiteName()
    }
    getSiteName(){
        //Define what site it is e.g. amazon:search, amazon:product
        this.siteName = "amazon:search"
    }
    getProducts(){
        var productPrice = "";
        var productName = "";
        var productArr = [];
        const placeholderImageURL = chrome.runtime.getURL("./icons/icon16.png")
        switch(this.siteName){
            case "amazon:search":
                // Query All Products
                //return document.querySelectorAll('div[role="listitem"]')
                const cardElements = document.querySelectorAll('div[data-asin][data-component-type="s-search-result"]')
                cardElements.forEach((cardElement) => {
                    // Scrape productName and productPrice
                    productName = cardElement.querySelector('h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal').innerText.trim();
                    try{
                        productPrice = cardElement.querySelector('span.a-offscreen').innerText.trim();
                    } catch(e) {
                        productPrice = "N/A"
                    }

                    // Generate product Unique Icon
                    // Avoid injecting multiple times
                    if(cardElement.querySelector(".sustainability-extension-icon")) return;
                    // Setting up icon properties (analysis is replaced with "Loading...")
                    let icon = document.createElement("img");
                    icon.src = placeholderImageURL; // sustainability icon
                    icon.className = "sustainability-extension-icon";
                    icon.style.width = "16px";
                    icon.style.height = "16px";
                    icon.style.position = "relative";
                    icon.style.top = "-220px";
                    icon.style.left = "-110px";
                    icon.style.cursor = "pointer";
                    icon.style.zIndex = "10";
                    icon.title = "Loading..."; // tooltip on hover

                    // Add click handler to icon
                    icon.addEventListener("click", () => {
                        alert("Loading...")
                    })
                    // Attach Icon to Product Image
                    cardElement.querySelector('div[class="a-section aok-relative s-image-square-aspect"]').appendChild(icon);
                    productArr.push(new ProductObj(productName,productPrice,icon));
                })
                // Query other products on website below vvv
                //
                return productArr
                break;
            case "shopee":
                // Query All Products
                    // Scrape productName and productPrice
                    // Generate product Unique Icon
                    // push ProductObj(productName,productPrice,icon)
                return null
            case "lazada":
                return null
            default:
                return null
        }
    }
}

