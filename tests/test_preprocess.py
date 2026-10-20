
import pandas as pd
from preprocess import normalize_ingredient, clean_recipes
from recommender_adapter import recommend


# Test ingredient cleaning
def test_ingredients():

    assert normalize_ingredient("tomatoes") == "tomato"
    assert normalize_ingredient("eggs") == "egg"
    assert normalize_ingredient("onions") == "onion"


# Test cleaning the recipe dataset
def test_dataset(tmp_path):

    input_file = tmp_path / "recipes.csv"
    output_file = tmp_path / "cleaned.csv"

    # Create sample recipes for testing
    recipes = [
        {
            "name": "Egg Dish",
            "ingredients": "eggs; tomato; onion",
            "instructions": "Cook the ingredients.",
            "country": "American"
        },
        {
            "name": "Missing Recipe",
            "ingredients": "salt",
            "instructions": "",
            "country": "American"
        }
    ]

    # Save sample recipes
    df = pd.DataFrame(recipes)
    df.to_csv(input_file, index=False)

    # Clean the dataset
    clean_recipes(input_file, output_file)

    cleaned = pd.read_csv(output_file)

    # Check that the incomplete recipe was removed
    assert len(cleaned) == 1

    # Check that the correct recipe remains
    assert cleaned.iloc[0]["title"] == "Egg Dish"


# Test recipe recommendations
def test_recommendations():

    # Create sample recipe data
    recipes = pd.DataFrame([
        {
            "title": "Egg Dish",
            "ingredients": '["egg", "tomato", "onion"]',
            "normalized_ingredients": '["egg", "tomato", "onion"]',
            "instructions": "Cook the ingredients.",
            "cuisine": "American"
        }
    ])

    # Search using ingredients
    results = recommend(recipes, ["egg", "tomato"])

    # Check the recommended recipe
    assert len(results) == 1
    assert results[0]["title"] == "Egg Dish"

    # Check the matching ingredients
    assert results[0]["matched"] == ["egg", "tomato"]

    # Check the missing ingredient
    assert results[0]["missing"] == ["onion"]
