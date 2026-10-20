"""Create a small original demonstration dataset (not a substitute for a full dataset)."""
import pandas as pd
from pathlib import Path
rows=[
('Tomato Egg Scramble','2 eggs; 1 tomato; 1 tbsp olive oil; salt; black pepper','Whisk eggs. Chop tomato. Heat oil, cook tomatoes for two minutes, add eggs, and stir until cooked.','Home-style'),
('Spinach Omelet','3 eggs; spinach; cheese; butter; salt','Beat eggs and pour into a buttered skillet. Add spinach and cheese; fold when set.','Breakfast'),
('Cheese Quesadilla','2 tortillas; cheddar cheese; 1 tomato; onion','Place cheese and diced vegetables between tortillas. Toast in a pan until golden.','Mexican'),
('Garlic Butter Pasta','pasta; 2 cloves garlic; butter; parsley; salt','Boil pasta until tender. Melt butter with minced garlic, toss with pasta and parsley.','Italian'),
('Tomato Basil Pasta','pasta; 3 tomatoes; fresh basil; olive oil; 2 cloves garlic','Cook pasta. Saute garlic and chopped tomatoes in oil. Toss with pasta and basil.','Italian'),
('Chicken Rice Bowl','chicken breast; rice; broccoli; soy sauce; garlic','Cook rice. Cook chicken thoroughly in a skillet with garlic. Steam broccoli and serve with soy sauce.','Asian-inspired'),
('Black Bean Tacos','black beans; tortillas; onion; tomato; cumin; lime','Warm beans with cumin. Spoon into tortillas and top with diced onion, tomato, and lime.','Mexican'),
('Greek Cucumber Salad','cucumber; tomato; feta cheese; olive oil; lemon','Chop cucumber and tomato. Toss with feta, olive oil, and lemon juice.','Mediterranean'),
('Banana Oat Pancakes','banana; oats; eggs; cinnamon; milk','Blend ingredients into a batter. Cook small pancakes on a lightly greased skillet until set.','Breakfast'),
('Vegetable Fried Rice','cooked rice; egg; carrot; peas; soy sauce; green onion','Scramble egg. Saute diced carrots and peas. Add cooked rice and soy sauce; finish with green onion.','Asian-inspired'),
('Baked Potato','potato; olive oil; salt; sour cream; green onion','Scrub and prick potato. Rub with oil and salt. Bake at 425 F until tender; top with sour cream and onion.','American'),
('Chickpea Tomato Stew','chickpeas; tomato; onion; garlic; cumin; olive oil','Cook chopped onion and garlic in olive oil. Add tomatoes, chickpeas, and cumin; simmer until thick.','Mediterranean'),
('Peanut Butter Banana Toast','bread; peanut butter; banana; cinnamon','Toast bread. Spread peanut butter and top with banana slices and cinnamon.','Breakfast'),
('Mushroom Risotto','arborio rice; mushroom; onion; vegetable broth; parmesan; butter','Saute onion and mushrooms. Stir in rice and add warm broth gradually until creamy. Finish with butter and parmesan.','Italian'),
('Avocado Egg Toast','bread; avocado; egg; lemon; salt','Toast bread. Mash avocado with lemon and salt. Cook egg thoroughly and place on top.','Breakfast'),
('Broccoli Cheese Soup','broccoli; cheddar cheese; milk; onion; vegetable broth; butter','Saute onion in butter. Add broccoli and broth, simmer until soft. Stir in milk and cheese.','American'),
('Lentil Soup','lentils; carrot; celery; onion; vegetable broth; cumin','Saute diced vegetables. Add lentils, cumin, and broth and simmer until lentils are tender.','Mediterranean'),
('Caprese Sandwich','bread; mozzarella; tomato; basil; olive oil','Layer mozzarella, sliced tomato, and basil on bread. Drizzle with olive oil.','Italian'),
('Apple Yogurt Parfait','apple; greek yogurt; oats; honey; cinnamon','Layer chopped apple, yogurt, and oats. Drizzle honey and sprinkle cinnamon.','Breakfast'),
('Tofu Stir Fry','tofu; bell pepper; broccoli; soy sauce; garlic; rice','Cook rice. Brown tofu in a pan. Saute vegetables and garlic, add soy sauce, and serve over rice.','Asian-inspired'),
('Vegetarian Burrito Bowl','rice; black beans; corn; tomato; avocado; lime','Cook rice. Warm beans and corn, then layer with tomato, avocado, and lime juice.','Mexican'),
('Simple Egg Salad','egg; mayonnaise; mustard; celery; salt','Hard-boil eggs and cool. Chop and combine with mayonnaise, mustard, diced celery, and salt.','American'),
('Roasted Carrot Soup','carrot; onion; vegetable broth; olive oil; garlic','Roast carrots until tender. Cook onion and garlic in oil, add broth and carrots, then blend.','American'),
('Berry Smoothie','banana; strawberries; blueberries; milk; yogurt','Blend fruit with milk and yogurt until smooth.','Breakfast'),
]
out=Path(__file__).resolve().parent/'data'/'sample_recipes.csv'
pd.DataFrame(rows,columns=['name','ingredients','instructions','country']).to_csv(out,index=False)
print(f'Created {len(rows)} demo recipes at {out}')
