import streamlit as st
import pandas as pd
from recommender_adapter import recommend
from preprocess import normalize_ingredient

# Set up the page
st.set_page_config(page_title="Smart Recipe Finder", page_icon="🥗")

st.title("🥗 Smart Recipe Finder")
st.write("Find recipes based on ingredients you already have!")

# Load recipe data
recipes = pd.read_csv("data/recipes_cleaned.csv").fillna("")

# Enter ingredients
st.header("Your Ingredients")

user_input = st.text_area(
    "Enter your ingredients separated by commas:",
    placeholder="Example: tomato, egg, onion, cheese"
)

ingredients = []

if user_input:
    for item in user_input.split(","):
        ingredient = normalize_ingredient(item)

        if ingredient:
            ingredients.append(ingredient)

# Upload a photo
st.header("Upload Ingredient Photo")

photo = st.file_uploader(
    "Choose a picture of your ingredients",
    type=["jpg", "jpeg", "png"]
)

if photo:
    st.image(photo, caption="Uploaded Photo")
    st.info("Image recognition will be added later.")

# Recipe preferences
st.header("Recipe Preferences")

cuisines = ["All"] + sorted(recipes["cuisine"].dropna().unique().tolist())

selected_cuisine = st.selectbox("Choose a cuisine:", cuisines)

number_of_recipes = st.slider(
    "Number of recipes to show:",
    1, 20, 5
)

# Find recipes
if st.button("Find Recipes"):

    if len(ingredients) == 0:
        st.warning("Please enter at least one ingredient.")

    else:
        results = recommend(
            recipes,
            ingredients,
            top_k=number_of_recipes,
            cuisine=selected_cuisine
        )

        st.header("Recommended Recipes")

        if len(results) == 0:
            st.write("No recipes found.")

        else:
            for recipe in results:

                st.subheader(recipe["title"])

                st.write(
                    "Ingredient Match:",
                    round(recipe["score"] * 100),
                    "%"
                )

                st.write("Ingredients you have:")
                st.write(", ".join(recipe["matched"]))

                st.write("Ingredients you need:")
                st.write(", ".join(recipe["missing"]))

                with st.expander("View Recipe"):
                    st.write("Ingredients:")
                    st.write(", ".join(recipe["ingredients"]))

                    st.write("Instructions:")
                    st.write(recipe["instructions"])

                st.divider()

st.caption("CPSC 481 - Smart Recipe Recommendation System")
