// Cache for storing API responses
const productCache = {};

// Message listener
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'PRODUCT_CLICK') {
    handleProductSearch(request.data);
  }
});

async function handleProductSearch(productData) {
  try {
    // 1. Search Open Food Facts for similar products
    const similarProducts = await searchOpenFoodFacts(productData.name);
    
    // 2. Get nutrition scores for the most similar product
    const currentProduct = findMostSimilar(productData.name, similarProducts);
    const currentScores = calculateScores(currentProduct);
    
    // 3. Find better alternatives
    const betterAlternatives = findBetterAlternatives(currentScores, similarProducts);
    
    // 4. Send to content script to display
    chrome.tabs.sendMessage(sender.tab.id, {
      type: 'SHOW_RECOMMENDATION',
      data: {
        currentScore: currentScores.total,
        betterScore: betterAlternatives[0].total,
        currentProduct,
        betterProduct: betterAlternatives[0]
      }
    });
    
  } catch (error) {
    console.error('Error processing product:', error);
  }
}

async function searchOpenFoodFacts(query) {
  const cacheKey = query.toLowerCase();
  if (productCache[cacheKey]) {
    return productCache[cacheKey];
  }
  
  const url = `https://world.openfoodfacts.org/cgi/search.pl?search_terms=${encodeURIComponent(query)}&search_simple=1&json=1`;
  
  const response = await fetch(url);
  const data = await response.json();
  
  productCache[cacheKey] = data.products;
  return data.products;
}

function findMostSimilar(amazonProductName, openFoodProducts) {
  // Implement fuzzy matching algorithm
  // Using Levenshtein distance for simplicity
  let bestMatch = null;
  let bestScore = Infinity;
  
  for (const product of openFoodProducts) {
    const distance = levenshteinDistance(amazonProductName, product.product_name || '');
    if (distance < bestScore) {
      bestScore = distance;
      bestMatch = product;
    }
  }
  
  return bestMatch;
}

function calculateScores(product) {
  // Calculate composite score based on:
  // - Nutri-Score (A-E)
  // - NOVA score (1-4)
  // - Eco-Score (A-E)
  
  const nutriScore = convertNutriScore(product.nutriscore_grade);
  const novaScore = product.nova_group || 4;
  const ecoScore = convertEcoScore(product.ecoscore_grade);
  
  return {
    nutriScore,
    novaScore,
    ecoScore,
    total: (nutriScore * 0.5) + (novaScore * 0.3) + (ecoScore * 0.2)
  };
}

function findBetterAlternatives(currentScores, products) {
  return products
    .map(p => ({
      product: p,
      scores: calculateScores(p)
    }))
    .filter(p => p.scores.total > currentScores.total)
    .sort((a, b) => b.scores.total - a.scores.total);
}

// Helper functions
function levenshteinDistance(a, b) {
  // Implement Levenshtein distance algorithm
  // (Implementation omitted for brevity)
}

function convertNutriScore(grade) {
  const scores = { 'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1 };
  return scores[grade?.toLowerCase()] || 1;
}

function convertEcoScore(grade) {
  const scores = { 'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1 };
  return scores[grade?.toLowerCase()] || 1;
}
