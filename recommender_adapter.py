
import json
from preprocess import normalize_ingredient


# Find recipes that match the user's ingredients
def recommend(recipes, user_ingredients, top_k=12, cuisine="All"):

    results = []

    # Clean the ingredients entered by the user
    available = []

    for ingredient in user_ingredients:
        clean = normalize_ingredient(ingredient)

        if clean != "" and clean not in available:
            available.append(clean)

    # Check each recipe in the dataset
    for index, row in recipes.iterrows():

        # Check the selected cuisine
        if cuisine != "All" and row["cuisine"] != cuisine:
            continue

        # Get the recipe ingredients
        ingredients = json.loads(row["ingredients"])
        needed = json.loads(row["normalized_ingredients"])

        matched = []
        missing = []

        # Compare the user's ingredients with the recipe
        for ingredient in needed:

            if ingredient in available:
                matched.append(ingredient)
            else:
                missing.append(ingredient)

        # Only recommend recipes with matching ingredients
        if len(matched) > 0:

            # Calculate the match percentage
            score = len(matched) / len(needed)

            recipe = {
                "title": row["title"],
                "ingredients": ingredients,
                "instructions": row["instructions"],
                "cuisine": row["cuisine"],
                "score": score,
                "matched": matched,
                "missing": missing
            }

            results.append(recipe)

    # Show recipes with the highest match percentage first
    results.sort(key=lambda recipe: recipe["score"], reverse=True)

    # Return the requested number of recipes
    return results[:top_k]
