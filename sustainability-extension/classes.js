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

/**
 * Extension to calculate sustainability score by product name
 */
import SustainabilityScorer from "../backend/world-food-facts-api.py"

class ProductObj {
    constructor() {
        //this.imgElement = imgElement;
        this.icon = null;
        this.name = "";
        this.price = "";
        this.analysis = null;
    }
    setName(productName){
        this.name = productName;
    }
    setPrice(productPrice){
        this.price = productPrice;
    }
    setIcon(productIcon){
        this.icon = productIcon;
    }
    setAnalysis(productAnalysis){
        this.analysis = productAnalysis;
    }
    getInfo(){
        return [this.name,this.price]
    }

    /**
     * Generate scores hashtable from SustainabilityScorer
     */
    async analyzeSustainability() {
        const response = await fetch("http://localhost:5000/score", {
            method: 'POST',
            headers: { 'Content-Type' : 'application/json' },
            body: JSON.stringify({ product_name: this.name })
        });
        return await response.json();
    }

    async getAnalysis(){
        const results = await this.analyzeSustainability();
        return results;
    }
    async updateIcon(){
        if (!this.analysis) {await this.getAnalysis()}
        const nameElement = document.querySelector(".analysis-name");
        const ecoElement = document.querySelector(".analysis-eco");
        const carbonElement = document.querySelector(".analysis-carbon");
        const packagingElement = document.querySelector(".analysis-packaging");
        const certificationElement = document.querySelector(".analysis-certification");
        const nutritionElement = document.querySelector(".analysis-nutrition");
        nameElement.innerHTML = `Name: ${this.name}`;
        ecoElement.innerHTML = `🌱 Eco: ${this.analysis.ecoScore}`;
        carbonElement.innerHTML = `👣 Carbon: ${this.analysis.carbonScore}`;
        packagingElement.innerHTML = `📦 Packaging: ${this.analysis.packagingScore}`;
        certificationElement.innerHTML = `📃 Certification: ${this.analysis.certificationScore}`;
        nutritionElement.innerHTML = `🍎 Nutrition: ${this.analysis.nutritionScore}`;

        const placeholderSustainabilityScore = 70;
        animateProgressBar(this.analysis.sustainabilityScore);
    }
    async showPopup(){
        event.stopPropagation();
        event.preventDefault();
        showModalPopup(analyticsHtml);
        this.updateIcon();
    }
}
class SiteObj {
    constructor(hostname,siteURL){
        this.hostname = hostname;
        this.url = siteURL;
        this.siteName = "";
        this.parseSiteName()
    }
    parseSiteName(){
        //Define what site it is e.g. amazon:search, amazon:product
        var siteName = "";
        // Shopping Site
        if (this.hostname.includes("amazon.")){
            siteName = "amazon";
        } else if (this.hostname.includes("shopee.")){
            siteName = "shopee";
        }

        // Site Location (search,product,etc.)
        if (this.url.includes("s?k=")){ //amazon:search
            siteName = siteName + ":search"
        }
        //console.log(siteName);
        this.siteName = siteName;
    }
    getSiteName() {
        return this.siteName
    }
    getProducts(){
        var productPrice = "";
        var productName = "";
        var productArr = [];
        const placeholderImageURL = chrome.runtime.getURL("./icons/favicon_leaf.png")
        switch(this.siteName){
            case "amazon:search": // ################ amazon:search ####################
                // Query All Products
                //return document.querySelectorAll('div[role="listitem"]')
                const cardElements = document.querySelectorAll('div[data-asin][data-component-type="s-search-result"]')
                cardElements.forEach((cardElement) => {
                    const productObj = new ProductObj();
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
                    icon.style.width = "24px";
                    icon.style.height = "24px";
                    icon.style.position = "relative";
                    icon.style.top = "-250px";
                    icon.style.left = "-120px";
                    icon.style.cursor = "pointer";
                    icon.style.zIndex = "9950";
                    icon.title = "Loading..."; // tooltip on hover

                    // Add click handler to icon

                    icon.addEventListener("click", () => {
                        /*
                        event.stopPropagation();
                        event.preventDefault();
                        const testHTML = `
                          <div class="product-popup">
                            <h3>Product Info</h3>
                            <p>Description, price, etc.</p>
                            <button>Buy Now</button>
                          </div>
                        `;
                        showModalPopup(testHTML);
                        */
                        productObj.showPopup()
                    })


                    // Attach Icon to Product Image
                    cardElement.querySelector('div[class="a-section aok-relative s-image-square-aspect"]').appendChild(icon);
                    productObj.setName(productName);
                    productObj.setPrice(productPrice);
                    productObj.setIcon(icon);
                    productArr.push(productObj);
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

