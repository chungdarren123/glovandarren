import requests
import time
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SustainabilityScore:
    """Data class for sustainability score results"""
    score: float
    breakdown: Dict[str, float]
    confidence: float
    missing_data: List[str]

class SustainabilityScorer:
    """Main class for calculating product sustainability scores"""
    
    def __init__(self, rate_limit_delay: float = 0.1):
        self.rate_limit_delay = rate_limit_delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SustainabilityScorer/1.0 (Educational)'
        })
    
    def get_product_data(self, product_name: str) -> Optional[Dict]:
        """
        Fetch product data from Open Food Facts API with better error handling
        
        Args:
            product_name: Name of the product to search for
            
        Returns:
            Product data dictionary or None if not found
        """
        try:
            url = "https://world.openfoodfacts.org/cgi/search.pl"
            params = {
                'search_terms': product_name,
                'json': 1,
                'page_size': 5  # Get top 5 matches for better selection
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("count", 0) > 0:
                # Find best match based on name similarity
                best_match = self._find_best_match(product_name, data["products"])
                if best_match:
                    logger.info(f"Found match: {best_match.get('product_name', 'Unknown')}")
                    return best_match
            
            logger.warning(f"No products found for: {product_name}")
            return None
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def _find_best_match(self, search_term: str, products: List[Dict]) -> Optional[Dict]:
        """Find the best matching product based on name similarity"""
        if not products:
            return None
        
        search_lower = search_term.lower()
        best_match = None
        best_score = 0
        
        for product in products:
            product_name = product.get('product_name', '').lower()
            if not product_name:
                continue
                
            # Simple similarity scoring
            score = 0
            words = search_lower.split()
            for word in words:
                if word in product_name:
                    score += 1
            
            similarity = score / len(words) if words else 0
            if similarity > best_score:
                best_score = similarity
                best_match = product
        
        return best_match if best_score > 0.3 else products[0]  # Fallback to first result
    
    def get_category_products(self, category: str, max_pages: int = 3, 
                            sample_size: int = 100) -> List[Dict]:
        """
        Fetch products from a category with better pagination and sampling
        
        Args:
            category: Product category
            max_pages: Maximum pages to fetch
            sample_size: Maximum products to return for analysis
            
        Returns:
            List of product dictionaries
        """
        products = []
        
        try:
            for page in range(1, max_pages + 1):
                if len(products) >= sample_size:
                    break
                    
                url = f"https://world.openfoodfacts.org/category/{category}/{page}.json"
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                page_products = data.get("products", [])
                if not page_products:
                    break
                    
                products.extend(page_products)
                logger.info(f"Fetched page {page}, total products: {len(products)}")
                
                # Rate limiting
                time.sleep(self.rate_limit_delay)
            
            # Return sample if we have too many products
            return products[:sample_size]
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch category products: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching category: {e}")
            return []
    
    def calculate_category_averages(self, products: List[Dict]) -> Dict[str, Union[float, str, None]]:
        """
        Calculate category averages with improved data handling
        
        Args:
            products: List of product dictionaries
            
        Returns:
            Dictionary of average values
        """
        if not products:
            return self._get_default_averages()
        
        indicators = {
            "ecoscore": [],
            "nutriscore": [],
            "carbon_footprint": [],
            "organic": 0,
            "fair_trade": 0,
            "recyclable": 0
        }
        
        total_products = len(products)
        
        for product in products:
            # Eco-Score
            ecoscore = product.get("ecoscore_grade", "").lower()
            if ecoscore in ['a', 'b', 'c', 'd', 'e']:
                indicators["ecoscore"].append(ecoscore)
            
            # Nutri-Score
            nutriscore = product.get("nutriscore_grade", "").lower()
            if nutriscore in ['a', 'b', 'c', 'd', 'e']:
                indicators["nutriscore"].append(nutriscore)
            
            # Carbon footprint - handle various field names
            nutriments = product.get("nutriments", {})
            co2_fields = ["carbon_footprint_per_100g", "carbon-footprint_per_100g", 
                         "carbon_footprint_100g"]
            
            for field in co2_fields:
                if field in nutriments:
                    try:
                        co2_value = float(nutriments[field])
                        if co2_value > 0:  # Only positive values
                            indicators["carbon_footprint"].append(co2_value)
                            break
                    except (ValueError, TypeError):
                        continue
            
            # Labels and certifications
            labels = product.get("labels", "")
            if isinstance(labels, list):
                labels = " ".join(labels)
            labels_lower = str(labels).lower()
            
            if any(term in labels_lower for term in ["organic", "bio", "biologique"]):
                indicators["organic"] += 1
            if any(term in labels_lower for term in ["fair trade", "fairtrade", "équitable"]):
                indicators["fair_trade"] += 1
            
            # Packaging
            packaging = product.get("packaging", "")
            if isinstance(packaging, list):
                packaging = " ".join(packaging)
            packaging_lower = str(packaging).lower()
            
            if "recyclable" in packaging_lower and "non-recyclable" not in packaging_lower:
                indicators["recyclable"] += 1
        
        # Calculate averages with fallbacks
        averages = {
            "avg_ecoscore": self._most_common(indicators["ecoscore"]) or "c",
            "avg_nutriscore": self._most_common(indicators["nutriscore"]) or "c",
            "avg_carbon_footprint": (
                sum(indicators["carbon_footprint"]) / len(indicators["carbon_footprint"]) 
                if indicators["carbon_footprint"] else 50.0  # Default fallback
            ),
            "organic_pct": (indicators["organic"] / total_products * 100) if total_products > 0 else 0,
            "fair_trade_pct": (indicators["fair_trade"] / total_products * 100) if total_products > 0 else 0,
            "recyclable_pct": (indicators["recyclable"] / total_products * 100) if total_products > 0 else 0,
            "sample_size": total_products
        }
        
        return averages
    
    def _most_common(self, lst: List) -> Optional[str]:
        """Find most common element in list"""
        if not lst:
            return None
        return max(set(lst), key=lst.count)
    
    def _get_default_averages(self) -> Dict[str, Union[float, str, None]]:
        """Return default averages when no category data is available"""
        return {
            "avg_ecoscore": "c",
            "avg_nutriscore": "c", 
            "avg_carbon_footprint": 50.0,
            "organic_pct": 10.0,
            "fair_trade_pct": 5.0,
            "recyclable_pct": 30.0,
            "sample_size": 0
        }
    
    def calculate_scores(self, product: Dict, category_averages: Dict) -> SustainabilityScore:
        """
        Calculate sustainability scores with improved logic and confidence tracking
        
        Args:
            product: Product data dictionary
            category_averages: Category average values
            
        Returns:
            SustainabilityScore object with score, breakdown, and metadata
        """
        scores = {}
        missing_data = []
        confidence_factors = []
        
        # Grade mapping
        grade_scores = {"a": 100, "b": 80, "c": 60, "d": 40, "e": 20}
        
        # 1. Eco-Score (30% weight)
        product_eco = product.get("ecoscore_grade", "").lower()
        category_eco = category_averages["avg_ecoscore"].lower()
        
        if product_eco in grade_scores:
            category_score = grade_scores[category_eco]
            product_score = grade_scores[product_eco]
            # Normalize against category average
            relative_score = min(100, (product_score / category_score) * 100)
            scores["eco"] = (relative_score / 100) * 30
            confidence_factors.append(0.9)  # High confidence for ecoscore
        else:
            scores["eco"] = 15  # Neutral score (50% of weight)
            missing_data.append("ecoscore")
            confidence_factors.append(0.3)
        
        # 2. Carbon Footprint (25% weight)
        nutriments = product.get("nutriments", {})
        co2_fields = ["carbon_footprint_per_100g", "carbon-footprint_per_100g"]
        product_co2 = None
        
        for field in co2_fields:
            if field in nutriments:
                try:
                    product_co2 = float(nutriments[field])
                    break
                except (ValueError, TypeError):
                    continue
        
        if product_co2 is not None and product_co2 > 0:
            category_co2 = category_averages["avg_carbon_footprint"]
            # Lower CO2 is better - inverse relationship
            if category_co2 > 0:
                ratio = product_co2 / category_co2
                # Scale: ratio < 0.5 gets full points, ratio > 2.0 gets minimum points
                carbon_score = max(0, min(100, 125 - (ratio * 50)))
                scores["carbon"] = (carbon_score / 100) * 25
                confidence_factors.append(0.8)
            else:
                scores["carbon"] = 12.5
                confidence_factors.append(0.4)
        else:
            scores["carbon"] = 12.5  # Neutral score
            missing_data.append("carbon_footprint")
            confidence_factors.append(0.3)
        
        # 3. Packaging (20% weight)
        packaging = product.get("packaging", "")
        if isinstance(packaging, list):
            packaging = " ".join(packaging)
        packaging_lower = str(packaging).lower()
        
        if packaging_lower:
            if "recyclable" in packaging_lower and "non-recyclable" not in packaging_lower:
                scores["packaging"] = 20
            elif "plastic" in packaging_lower or "non-recyclable" in packaging_lower:
                scores["packaging"] = 5
            else:
                scores["packaging"] = 10  # Unknown packaging gets neutral score
            confidence_factors.append(0.7)
        else:
            scores["packaging"] = 10
            missing_data.append("packaging")
            confidence_factors.append(0.2)
        
        # 4. Certifications (15% weight)
        labels = product.get("labels", "")
        if isinstance(labels, list):
            labels = " ".join(labels)
        labels_lower = str(labels).lower()
        
        cert_score = 0
        if labels_lower:
            if any(term in labels_lower for term in ["organic", "bio", "biologique"]):
                cert_score += 10
            if any(term in labels_lower for term in ["fair trade", "fairtrade", "équitable"]):
                cert_score += 5
            confidence_factors.append(0.8)
        else:
            missing_data.append("certifications")
            confidence_factors.append(0.3)
        
        scores["certifications"] = min(15, cert_score)
        
        # 5. Nutri-Score (10% weight)
        product_nutri = product.get("nutriscore_grade", "").lower()
        if product_nutri in grade_scores:
            scores["nutrition"] = (grade_scores[product_nutri] / 100) * 10
            confidence_factors.append(0.8)
        else:
            scores["nutrition"] = 5  # Neutral score
            missing_data.append("nutriscore")
            confidence_factors.append(0.3)
        
        # Calculate final score and confidence
        total_score = sum(scores.values())
        confidence = sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5
        
        return SustainabilityScore(
            score=min(100, max(0, total_score)),
            breakdown=scores,
            confidence=confidence,
            missing_data=missing_data
        )
    
    def analyze_product(self, product_name: str, category: str) -> Optional[SustainabilityScore]:
        """
        Complete analysis pipeline for a product
        
        Args:
            product_name: Name of the product to analyze
            category: Product category
            
        Returns:
            SustainabilityScore object or None if analysis failed
        """
        logger.info(f"Analyzing product: {product_name} in category: {category}")
        
        # Get product data
        product_data = self.get_product_data(product_name)
        if not product_data:
            logger.error("Could not find product data")
            return None
        
        # Get category benchmarks
        logger.info("Fetching category benchmarks...")
        category_products = self.get_category_products(category)
        category_averages = self.calculate_category_averages(category_products)
        
        logger.info(f"Category analysis based on {category_averages['sample_size']} products")
        
        # Calculate scores
        result = self.calculate_scores(product_data, category_averages)
        
        logger.info(f"Analysis complete. Score: {result.score:.1f}, Confidence: {result.confidence:.2f}")
        if result.missing_data:
            logger.warning(f"Missing data for: {', '.join(result.missing_data)}")
        
        return result


def main():
    """Example usage of the improved sustainability scorer"""
    scorer = SustainabilityScorer()
    
    # Example analysis
    product_name = "heineken"
    category = "alcohol"
    
    result = scorer.analyze_product(product_name, category)
    
    if result:
        print(f"\n=== Sustainability Analysis Results ===")
        print(f"Product: {product_name}")
        print(f"Overall Score: {result.score:.1f}/100")
        print(f"Confidence: {result.confidence:.1%}")
        
        print(f"\n--- Score Breakdown ---")
        for component, score in result.breakdown.items():
            print(f"{component.capitalize()}: {score:.1f}")
        
        if result.missing_data:
            print(f"\n--- Missing Data ---")
            print(f"Components with limited data: {', '.join(result.missing_data)}")
        
        print(f"\n--- Interpretation ---")
        if result.score >= 80:
            print("🌟 Excellent sustainability profile")
        elif result.score >= 60:
            print("✅ Good sustainability profile")
        elif result.score >= 40:
            print("⚠️ Average sustainability profile")
        else:
            print("❌ Below average sustainability profile")
    else:
        print("Analysis failed - could not retrieve product data")


if __name__ == "__main__":
    main()