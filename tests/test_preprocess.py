import pandas as pd
from preprocess import normalize_ingredient, clean_recipes

def test_ingredients(): # test ingredient cleaning
    assert normalize_ingredient("tomatoes") == "tomato" # check plural
    assert normalize_ingredient("2 eggs") == "egg" # check quantity
    assert normalize_ingredient("1/2 cup onions") == "onion" # check measurement


def test_dataset(tmp_path): # test dataset cleaning
    input_file = tmp_path / "recipes.csv" # original file
    output_file = tmp_path / "cleaned.csv" # cleaned file

    recipes = [ # sample recipes for testing
        {
            "name": "Egg Dish",
            "ingredients": "eggs; tomato; onion",
            "instructions": "Cook everything.",
            "country": "American"
        },
        {
            "name": "Missing Recipe",
            "ingredients": "salt",
            "instructions": "",
            "country": "American"
        }
    ]

    pd.DataFrame(recipes).to_csv(input_file, index=False) # save sample CSV
    clean_recipes(input_file, output_file) # clean recipes
    cleaned = pd.read_csv(output_file) # read cleaned CSV

    assert len(cleaned) == 1 # check incomplete recipe removed
    assert cleaned.iloc[0]["title"] == "Egg Dish" # check correct recipe