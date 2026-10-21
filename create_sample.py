import pandas as pd
import os

# Sample recipes for testing our application
# Each recipe has a name, ingredients, instructions, and cuisine

recipes = [
    ["Tomato Egg Scramble", "eggs; tomato; olive oil; salt; pepper",
     "Cook tomatoes in a pan, add eggs, and stir until cooked.", "Home-style"],

    ["Spinach Omelet", "eggs; spinach; cheese; butter; salt",
     "Cook eggs in a pan, add spinach and cheese, then fold.", "Breakfast"],

    ["Cheese Quesadilla", "tortillas; cheese; tomato; onion",
     "Add cheese and vegetables between tortillas and cook in a pan.", "Mexican"],

    ["Garlic Butter Pasta", "pasta; garlic; butter; parsley; salt",
     "Boil pasta and mix with melted garlic butter.", "Italian"],

    ["Tomato Basil Pasta", "pasta; tomato; basil; olive oil; garlic",
     "Cook pasta and mix with tomatoes, garlic, and basil.", "Italian"],

    ["Chicken Rice Bowl", "chicken; rice; broccoli; soy sauce; garlic",
     "Cook chicken, rice, and broccoli, then combine.", "Asian-inspired"],

    ["Black Bean Tacos", "black beans; tortillas; onion; tomato; cumin; lime",
     "Heat beans and serve in tortillas with vegetables.", "Mexican"],

    ["Greek Cucumber Salad", "cucumber; tomato; feta cheese; olive oil; lemon",
     "Chop vegetables and mix with feta cheese and olive oil.", "Mediterranean"],

    ["Banana Oat Pancakes", "banana; oats; eggs; cinnamon; milk",
     "Mix ingredients into a batter and cook pancakes.", "Breakfast"],

    ["Vegetable Fried Rice", "rice; egg; carrot; peas; soy sauce; green onion",
     "Cook vegetables and egg, then mix with rice and soy sauce.", "Asian-inspired"],

    ["Baked Potato", "potato; olive oil; salt; sour cream; green onion",
     "Bake potato until tender and add toppings.", "American"],

    ["Chickpea Tomato Stew", "chickpeas; tomato; onion; garlic; cumin; olive oil",
     "Cook onion and garlic, then add tomatoes and chickpeas.", "Mediterranean"],

    ["Peanut Butter Banana Toast", "bread; peanut butter; banana; cinnamon",
     "Toast bread and add peanut butter and banana.", "Breakfast"],

    ["Mushroom Risotto", "rice; mushroom; onion; vegetable broth; parmesan; butter",
     "Cook rice with mushrooms and gradually add broth.", "Italian"],

    ["Avocado Egg Toast", "bread; avocado; egg; lemon; salt",
     "Toast bread and top with avocado and cooked egg.", "Breakfast"],

    ["Broccoli Cheese Soup", "broccoli; cheese; milk; onion; vegetable broth; butter",
     "Cook broccoli and onion in broth, then add milk and cheese.", "American"],

    ["Lentil Soup", "lentils; carrot; celery; onion; vegetable broth; cumin",
     "Cook vegetables and lentils in broth until soft.", "Mediterranean"],

    ["Caprese Sandwich", "bread; mozzarella; tomato; basil; olive oil",
     "Add mozzarella, tomato, and basil between bread.", "Italian"],

    ["Apple Yogurt Parfait", "apple; yogurt; oats; honey; cinnamon",
     "Layer apple, yogurt, and oats, then add honey.", "Breakfast"],

    ["Tofu Stir Fry", "tofu; bell pepper; broccoli; soy sauce; garlic; rice",
     "Cook tofu and vegetables, then serve with rice.", "Asian-inspired"],

    ["Vegetarian Burrito Bowl", "rice; black beans; corn; tomato; avocado; lime",
     "Combine cooked rice, beans, corn, and vegetables.", "Mexican"],

    ["Simple Egg Salad", "egg; mayonnaise; mustard; celery; salt",
     "Boil eggs, chop them, and mix with mayonnaise and mustard.", "American"],

    ["Roasted Carrot Soup", "carrot; onion; vegetable broth; olive oil; garlic",
     "Cook carrots, onion, and garlic, then blend with broth.", "American"],

    ["Berry Smoothie", "banana; strawberries; blueberries; milk; yogurt",
     "Blend all ingredients until smooth.", "Breakfast"]
]

# Create a folder for the dataset
os.makedirs("data", exist_ok=True)

# Convert the recipes into a DataFrame
df = pd.DataFrame(
    recipes,
    columns=["name", "ingredients", "instructions", "country"]
)

# Save the recipes as a CSV file
df.to_csv("data/sample_recipes.csv", index=False)

print("Sample recipe dataset created successfully!")
print("Total recipes:", len(df))
