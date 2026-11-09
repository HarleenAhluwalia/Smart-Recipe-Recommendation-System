import json
from preprocess import normalize_ingredient


def recommend(recipes, user_ingredients, top_k=12, cuisine="All"):

    results = []
    available = []

    for ingredient in user_ingredients:
        clean = normalize_ingredient(ingredient)
        if clean != "" and clean not in available:
            available.append(clean)

    for index, row in recipes.iterrows():
        if cuisine != "All" and row["cuisine"] != cuisine:
            continue

        ingredients = json.loads(row["ingredients"]) # this includes measurments
        needed = json.loads(row["normalized_ingredients"]) # this just used everything as a single ingrediant

        matched = []
        missing = []

        for ingredient in needed:
            if ingredient in available:
                matched.append(ingredient)
            else:
                missing.append(ingredient)

        if len(matched) > 0:
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

    results.sort(key=lambda recipe: recipe["score"], reverse=True)

    return results[:top_k]