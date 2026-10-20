import json
from pathlib import Path
import pandas as pd
from preprocess import clean_recipes,normalize_ingredient,split_ingredients
from recommender_adapter import recommend

def test_normalization():
    assert normalize_ingredient('2 cloves garlic, minced') == 'garlic'
    assert normalize_ingredient('3 tomatoes, chopped') == 'tomato'

def test_parsing():
    assert len(split_ingredients("['1 egg', '2 tomatoes']")) == 2
    assert len(split_ingredients('egg; tomato; onion')) == 3

def test_clean_and_match(tmp_path):
    source=tmp_path/'raw.csv'; output=tmp_path/'clean.csv'
    pd.DataFrame([{'name':'Egg dish','ingredients':'2 eggs; tomato; onion','instructions':'Cook well.','country':'Test'},
                  {'name':'Incomplete','ingredients':'salt','instructions':'','country':'Test'}]).to_csv(source,index=False)
    assert clean_recipes(source,output)==1
    df=pd.read_csv(output)
    results=recommend(df,['egg','tomato'])
    assert results[0]['title']=='Egg dish'
    assert results[0]['matched']==['egg','tomato']
    assert results[0]['missing']==['onion']
