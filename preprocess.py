"""Clean source recipes into a stable schema for the application."""
import argparse
import ast
import json
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
MEASURE = re.compile(r'^(?:\d+(?:[./]\d+)?\s*|[¼½¾⅓⅔⅛⅜⅝⅞]\s*|a\s+|an\s+|one\s+|two\s+|pinch\s+(?:of\s+)?|to\s+taste\s*|\d+\s*[-–]\s*\d+\s*)+', re.I)
UNITS = re.compile(r'^(?:(?:cups?|tablespoons?|tbsp|teaspoons?|tsp|grams?|g|kg|oz|ounces?|lbs?|pounds?|ml|l|liters?|cloves?|cans?|packages?|slices?|pieces?|bunches?|stalks?|medium|large|small)\b\.?\s*)+', re.I)
ALIASES = {'tomatoes':'tomato','potatoes':'potato','eggs':'egg','onions':'onion','carrots':'carrot','bananas':'banana','apples':'apple','garlic cloves':'garlic','scallions':'green onion','spring onions':'green onion','bell peppers':'bell pepper','chickpeas':'chickpea','mushrooms':'mushroom','black beans':'black bean'}

def normalize_ingredient(value):
    s = str(value).lower().strip()
    s = re.sub(r'\([^)]*\)', '', s)
    s = MEASURE.sub('', s)
    s = UNITS.sub('', s)
    s = re.sub(r'\b(?:fresh|frozen|chopped|diced|minced|sliced|peeled|boneless|skinless|optional|roughly|finely|of|some)\b', ' ', s)
    s = re.split(r'[,;]', s)[0]
    s = re.sub(r'[^a-z\s-]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip(' -')
    return ALIASES.get(s, s)

def split_ingredients(value):
    if isinstance(value, list):
        raw = value
    else:
        value = str(value).strip()
        if value.startswith('['):
            try:
                parsed = ast.literal_eval(value)
                raw = parsed if isinstance(parsed, list) else [value]
            except (ValueError, SyntaxError):
                raw = [value]
        elif ';' in value:
            raw = value.split(';')
        elif '|' in value:
            raw = value.split('|')
        else:
            raw = [value]
    return [str(x).strip() for x in raw if str(x).strip() and str(x).strip().lower() != 'nan']

def clean_recipes(input_path, output_path):
    df = pd.read_csv(input_path, encoding='utf-8-sig', on_bad_lines='skip').fillna('')
    cols = {c.lower().strip(): c for c in df.columns}
    def get(row, *names):
        return next((row[cols[n]] for n in names if n in cols), '')
    if not any(n in cols for n in ('name','title','recipe_name')) or not any(n in cols for n in ('ingredients','ingredient')):
        raise ValueError(f'Expected name/title and ingredients columns. Found: {list(df.columns)}')
    records, seen = [], set()
    for _, row in df.iterrows():
        title = str(get(row, 'name','title','recipe_name')).strip()
        raw = split_ingredients(get(row, 'ingredients','ingredient'))
        normalized = list(dict.fromkeys(filter(None, (normalize_ingredient(x) for x in raw))))
        instructions = str(get(row,'instructions','directions','steps','description')).strip()
        if not title or len(normalized) < 2 or not instructions or title.lower() in seen:
            continue
        seen.add(title.lower())
        records.append({'recipe_id':len(records)+1, 'title':title, 'ingredients':json.dumps(raw, ensure_ascii=False),
                        'normalized_ingredients':json.dumps(normalized, ensure_ascii=False),
                        'instructions':instructions, 'cuisine':str(get(row,'country','cuisine','region')).strip()})
    if not records:
        raise ValueError('No valid recipes remain after preprocessing')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(output_path, index=False)
    print(f'Input: {len(df)} rows | Cleaned: {len(records)} rows | Removed: {len(df)-len(records)}')
    print(f'Saved: {output_path}')
    return len(records)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Normalize recipe CSV data')
    p.add_argument('--input', type=Path, default=ROOT/'data'/'sample_recipes.csv')
    p.add_argument('--output', type=Path, default=ROOT/'data'/'recipes_cleaned.csv')
    a=p.parse_args()
    clean_recipes(a.input,a.output)
