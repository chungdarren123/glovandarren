# How to use world-food-facts-api.py

1. Import SustainabilityScorer class
2. Create an instance of the class
3. Use the function analyze_product(product_name) to generate the scores

## Properties of result

- result.score: Sustainability Score
- result.confidence: Confidence level of estimate
- result.breakdown: Dictionary of component-score pairs, for components of Eco, Carbon, Packaging, Certifications and Nutrition
- result.missing_data: Missing data of product components in API

## Example usage

from world-food-facts-api.py import SustainabilityScorer

scorer = SustainabilityScorer()  
result = scorer.analyze_product("Heineken Beer")
