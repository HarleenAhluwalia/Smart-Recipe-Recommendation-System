import streamlit as st
import pandas as pd
from preprocess import normalize_ingredient
from recommender_adapter import recommend
import anthropic
from image_recognition import build_vocabulary, detect_ingredients

@st.cache_resource
def get_client():
    return anthropic.Anthropic()

@st.cache_data(show_spinner=False)
def cached_detect(image_bytes, vocabulary):
    found = detect_ingredients(image_bytes, list(vocabulary), client=get_client())
    return [(d.name, d.confidence) for d in found]

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

vocabulary = build_vocabulary(recipes)
st.header("Ingredient Photo")
source = st.radio("Photo source:", ["Upload", "Camera"], horizontal=True)
if source == "Upload":
    photo = st.file_uploader("Upload a photo of your ingredients:", type=["jpg", "jpeg", "png", "webp"])
else:
    photo = st.camera_input("Take a photo of your ingredients:")

photo_ingredients = []
if photo:
    st.image(photo)
    detected = []
    try:
        with st.spinner("Identififying ingredients..."):
            detected = cached_detect(photo.getvalue(), tuple(vocabulary))
    except anthropic.AuthenticationError:
        st.error("Authentication error. Please check your API key.")
    except anthropic.RateLimitError:
        st.error("Rate limit exceeded. Please try again later.")
    except anthropic.APIConnectionError:
        st.error("API connection error. Please check your internet connection.")
    except anthropic.APIStatusError as e:
        st.error(f"API status error: {e}")
    except anthropic.AnthropicError as e:
        st.error(f"Anthropic error: {e}")

    if not detected:
        st.info("No ingredients detected. Please try again with a clearer photo, or add them manually below.")
    photo_ingredients = st.multiselect(
        "Ingredients found in your photo (add or remove as needed):",
        options=vocabulary,
        default=[name for name, _ in detected],
    )

all_ingredients = list(dict.fromkeys(ingredients + photo_ingredients))  # remove duplicates

st.header("Recipe Preferences")
cuisines = ["All"] + sorted(recipes["cuisine"].unique()) # get cuisines
cuisine = st.selectbox("Choose a cuisine:", cuisines) # choose cuisine
number = st.slider("Number of recipes:", 1, 20, 5) # choose number

if st.button("Find Recipes"): # search button

    if len(all_ingredients) == 0:
        st.warning("Please enter ingredients.")

    else:
        results = recommend(recipes, all_ingredients, number, cuisine) # find recipes
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
