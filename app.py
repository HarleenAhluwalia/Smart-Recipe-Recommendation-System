"""Streamlit UI for CPSC 481 Smart Recipe Recommendation System."""
import json
from pathlib import Path
import pandas as pd
import streamlit as st
from recommender_adapter import recommend
from preprocess import normalize_ingredient

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'/'recipes_cleaned.csv'
st.set_page_config(page_title='Smart Recipe Finder',page_icon='🥗',layout='wide')
st.markdown('''<style>
.block-container{padding-top:2rem;max-width:1250px}
.hero{background:linear-gradient(120deg,#17392e,#32704c);color:#fff;padding:32px;border-radius:22px;margin-bottom:22px}
.hero h1{font-size:2.4rem;margin:0 0 6px;color:white}.hero p{color:#ecf5ec;font-size:1.1rem;margin:0}
.note{background:#f4f8f3;border-left:4px solid #448a61;padding:12px 16px;border-radius:8px;color:#183c2d}
</style>''', unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🥗 Smart Recipe Finder</h1><p>Turn the ingredients in your kitchen into meal ideas.</p></div>',unsafe_allow_html=True)

@st.cache_data
def load_data():
    if not DATA.exists():
        return pd.DataFrame()
    return pd.read_csv(DATA).fillna('')

recipes=load_data()
if recipes.empty:
    st.error('Dataset not found. Run `python preprocess.py` in your terminal first.')
    st.stop()

left,right=st.columns([1,2],gap='large')
with left:
    st.subheader('Your kitchen')
    raw=st.text_area('What ingredients do you have?',placeholder='Example: tomato, egg, onion, cheese',height=140,help='Separate ingredients with commas or new lines.')
    chosen=[normalize_ingredient(x) for x in raw.replace('\n',',').split(',') if normalize_ingredient(x)]
    if chosen:
        st.caption('Recognized ingredients')
        st.write(' · '.join(dict.fromkeys(chosen)))
    st.divider()
    st.subheader('Ingredient photo')
    photo=st.file_uploader('Upload a photo (JPG or PNG)',type=['jpg','jpeg','png'])
    if photo:
        st.image(photo,caption='Photo uploaded',use_container_width=True)
        st.info('Photo detection is not connected yet. Avery will integrate the image model. Enter detected ingredients above for now.')
    st.divider()
    st.subheader('Preferences')
    options=['All']+sorted({str(x).strip() for x in recipes['cuisine'].tolist() if str(x).strip()})
    cuisine=st.selectbox('Cuisine',options)
    max_missing=st.slider('Maximum missing ingredients',0,20,20,help='Limit recipes that require too many extra items.')
    num_results=st.slider('Number of results',3,20,9)
    search=st.button('Find my recipes',type='primary',use_container_width=True)

with right:
    st.subheader('Recipe recommendations')
    if not search:
        st.markdown('<div class="note">Enter ingredients on the left, then choose <b>Find my recipes</b> to see matches.</div>',unsafe_allow_html=True)
        st.caption(f'{len(recipes):,} cleaned recipes loaded · Baseline ingredient-overlap matching (Jesse’s AI recommender can replace this).')
    elif not chosen:
        st.warning('Please add at least one ingredient to find recipes.')
    else:
        matches=recommend(recipes,chosen,top_k=len(recipes),cuisine=cuisine)
        matches=[r for r in matches if len(r['missing'])<=max_missing][:num_results]
        st.caption(f'{len(matches)} recipes displayed · Ranked by ingredient coverage. Scores are not nutritional or dietary-safety ratings.')
        if not matches:
            st.info('No matches for these filters. Add another ingredient or increase the missing-ingredient limit.')
        for recipe in matches:
            with st.container(border=True):
                c1,c2=st.columns([3,1])
                c1.markdown(f"#### {recipe['title']}")
                c2.metric('Ingredient match',f"{recipe['score']:.0%}")
                st.progress(recipe['score'])
                st.markdown('**You have:** '+(', '.join(recipe['matched']) if recipe['matched'] else 'None'))
                st.markdown('**Still needed:** '+(', '.join(recipe['missing']) if recipe['missing'] else 'Nothing — all listed ingredients matched!'))
                with st.expander('View full recipe'):
                    st.markdown('**Ingredient list**')
                    for item in recipe['ingredients']:
                        st.write('• '+item)
                    st.markdown('**Directions**')
                    st.write(recipe['instructions'])
                    if recipe['cuisine']:
                        st.caption('Cuisine / origin: '+recipe['cuisine'])

st.divider()
st.caption('CPSC 481 group project · UI & dataset: Harleen · Recommendation model: Jesse · Image recognition: Avery')
