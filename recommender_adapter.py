import json
import math
from collections import Counter
from preprocess import normalize_ingredient


def recommend(recipes, user_ingredients, top_k=12, cuisine="All"):

    counts = Counter(i for raw in recipes["normalized_ingredients"] for i in set(json.loads(raw)))
    idf = {i: math.log((len(recipes) + 1) / (n + 1)) + 1 for i, n in counts.items()}

    results = []
    available = []

    for ingredient in user_ingredients:
        clean = normalize_ingredient(ingredient)
        if clean != "" and clean not in available:
            available.append(clean)

    for index, row in recipes.iterrows():
        if cuisine != "All" and row["cuisine"] != cuisine:
            continue

        ingredients = json.loads(row["ingredients"])
        needed = json.loads(row["normalized_ingredients"])

        matched = []
        missing = []

        for ingredient in needed:
            if ingredient in available:
                matched.append(ingredient)
            else:
                missing.append(ingredient)

        if len(matched) > 0:
            score = sum(idf[i] for i in matched) / sum(idf[i] for i in needed)
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