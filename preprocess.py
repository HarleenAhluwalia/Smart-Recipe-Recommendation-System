import pandas as pd
import json


def normalize_ingredient(ingredient): # clean ingredient names
    ingredient = str(ingredient).lower().strip() # lowercase
    ingredient = ingredient.split(",")[0] # remove descriptions
    words = []

    for word in ingredient.split(): # check each word
        if word.replace("/", "").isdigit(): # skip numbers
            continue

        if word in ["cup", "cups", "tbsp", "tsp"]: # skip measurements
            continue

        words.append(word) # keep other words

    ingredient = " ".join(words) # combine words
    if ingredient == "eggs":
        ingredient = "egg"

    if ingredient == "tomatoes":
        ingredient = "tomato"

    if ingredient == "onions":
        ingredient = "onion"

    if ingredient == "tortillas":
        ingredient = "tortilla"

    return ingredient


def clean_recipes(input_file, output_file): # clean recipe data
    df = pd.read_csv(input_file).fillna("") # read CSV file
    cleaned = []

    for index, row in df.iterrows(): # go through each recipe
        name = row["name"]
        ingredients = row["ingredients"].split(";")
        instructions = row["instructions"]
        cuisine = row["country"]

        if name == "" or instructions == "": # skip missing information
            continue

        new_ingredients = []

        for item in ingredients:
            item = normalize_ingredient(item) # clean ingredient

            if item != "":
                new_ingredients.append(item)

        if len(new_ingredients) < 2: # skip recipes with less than 2 ingredients
            continue

        cleaned.append({
            "recipe_id": len(cleaned) + 1,
            "title": name,
            "ingredients": json.dumps(ingredients),
            "normalized_ingredients": json.dumps(new_ingredients),
            "instructions": instructions,
            "cuisine": cuisine
        })

    pd.DataFrame(cleaned).to_csv(output_file, index=False) # save cleaned CSV
    print("Cleaned recipes:", len(cleaned)) # show total

    return len(cleaned)