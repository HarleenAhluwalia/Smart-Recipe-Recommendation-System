"""Temporary, transparent ingredient-overlap baseline. Jesse can replace recommend()."""
import json
import pandas as pd
from preprocess import normalize_ingredient

def recommend(recipes: pd.DataFrame, user_ingredients: list[str], top_k: int = 12, cuisine: str = 'All') -> list[dict]:
    """Return list of {'title', 'ingredients', 'instructions', 'score', 'matched', 'missing', 'cuisine'}.

    Jesse: replace implementation with TF-IDF/cosine similarity while preserving contract.
    """
    available = {normalize_ingredient(item) for item in user_ingredients if normalize_ingredient(item)}
    results=[]
    for row in recipes.to_dict('records'):
        if cuisine != 'All' and str(row.get('cuisine','')).strip() != cuisine:
            continue
        ingredients=json.loads(row['ingredients'])
        needed=set(json.loads(row['normalized_ingredients']))
        matched=sorted(available & needed)
        if not matched:
            continue
        missing=sorted(needed - available)
        score=len(matched)/len(needed) if needed else 0
        results.append({**row,'ingredients':ingredients,'score':score,'matched':matched,'missing':missing})
    return sorted(results, key=lambda r:(-r['score'],-len(r['matched']),r['title']))[:top_k]
