import streamlit as st
import pandas as pd
from preprocess import normalize_ingredient
from recommender_adapter import recommend

st.title("Smart Recipe Finder")
st.write("Find recipes using ingredients you already have!")

recipes = pd.read_csv("data/recipes_cleaned.csv").fillna("") # read recipes

st.header("Your Ingredients")
user_input = st.text_area("Enter ingredients separated by commas:")
ingredients = []

for item in user_input.split(","): # separate ingredients
    item = normalize_ingredient(item) # clean ingredient

    if item != "":
        ingredients.append(item)

st.header("Recipe Preferences")
cuisines = ["All"] + sorted(recipes["cuisine"].unique()) # get cuisines
cuisine = st.selectbox("Choose a cuisine:", cuisines) # choose cuisine
number = st.slider("Number of recipes:", 1, 20, 5) # choose number

if st.button("Find Recipes"): # search button

    if len(ingredients) == 0:
        st.warning("Please enter ingredients.")

    else:
        results = recommend(recipes, ingredients, number, cuisine) # find recipes
        st.header("Recommended Recipes")

        if len(results) == 0:
            st.write("No recipes found.")

        for recipe in results: # show each recipe
            st.subheader(recipe["title"]) # recipe name
            st.write("Match score:", round(recipe["score"] * 100), "%")
            st.write("You have:", ", ".join(recipe["matched"]))
            st.write("You need:", ", ".join(recipe["missing"]))

            with st.expander("View Recipe"): # recipe details
                st.write("Ingredients:", ", ".join(recipe["ingredients"]))
                st.write("Instructions:", recipe["instructions"])
            st.divider()