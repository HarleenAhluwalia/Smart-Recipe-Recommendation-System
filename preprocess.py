import pandas as pd
import json
import os

# Clean ingredient names so they are easier to compare
def normalize_ingredient(ingredient):
    ingredient = str(ingredient).lower().strip()

    # Remove common measurements
    words_to_remove = [
        "cups", "cup", "tbsp", "tsp",
        "tablespoon", "teaspoon", "cloves", "clove"
    ]

    words = ingredient.split()
    clean_words = []

    for word in words:
        if word.isdigit():
            continue

        if word in words_to_remove:
            continue

        clean_words.append(word)

    ingredient = " ".join(clean_words)

    # Make common ingredient names consistent
    replacements = {
        "tomatoes": "tomato",
        "potatoes": "potato",
        "eggs": "egg",
        "onions": "onion",
        "carrots": "carrot",
        "bananas": "banana",
        "mushrooms": "mushroom",
        "chickpeas": "chickpea"
    }

    if ingredient in replacements:
        ingredient = replacements[ingredient]

    return ingredient


# Clean the recipe dataset
def clean_recipes(input_file, output_file):

    # Read the original CSV file
    df = pd.read_csv(input_file).fillna("")

    cleaned_recipes = []
    recipe_names = []

    # Go through each recipe
    for index, row in df.iterrows():

        name = str(row["name"]).strip()
        ingredients = str(row["ingredients"]).split(";")
        instructions = str(row["instructions"]).strip()
        cuisine = str(row["country"]).strip()

        # Skip recipes with missing information
        if name == "" or instructions == "":
            continue

        # Skip duplicate recipes
        if name.lower() in recipe_names:
            continue

        # Clean each ingredient
        clean_ingredients = []

        for ingredient in ingredients:
            cleaned = normalize_ingredient(ingredient)

            if cleaned != "" and cleaned not in clean_ingredients:
                clean_ingredients.append(cleaned)

        # Skip recipes with fewer than two ingredients
        if len(clean_ingredients) < 2:
            continue

        recipe_names.append(name.lower())

        # Save the cleaned recipe
        cleaned_recipes.append({
            "recipe_id": len(cleaned_recipes) + 1,
            "title": name,
            "ingredients": json.dumps(ingredients),
            "normalized_ingredients": json.dumps(clean_ingredients),
            "instructions": instructions,
            "cuisine": cuisine
        })

    # Create the data folder if needed
    os.makedirs("data", exist_ok=True)

    # Save the cleaned dataset
    cleaned_df = pd.DataFrame(cleaned_recipes)
    cleaned_df.to_csv(output_file, index=False)

    print("Dataset cleaned successfully!")
    print("Total recipes:", len(cleaned_df))


# Run the program
if __name__ == "__main__":
    clean_recipes(
        "data/sample_recipes.csv",
        "data/recipes_cleaned.csv"
    )
