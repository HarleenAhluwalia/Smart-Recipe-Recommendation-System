# Harleen's CPSC 481 contribution

## Completed
- Researched a public recipe dataset containing recipe names, ingredients, instructions, and country information.
- Built a reproducible Python/Pandas cleaning script (column handling, parsing, deduplication, normalization, and CSV export).
- Created a small original 24-recipe demo CSV and generated its cleaned version, so the app can be demonstrated offline.
- Built a Streamlit UI with manual ingredient entry, photo-upload preview, cuisine selection, missing-ingredient filter, match scores, and full recipe instructions.
- Wrote installation instructions and regression tests; included defined handoff boundaries for teammates.

## What Jesse should do
- Replace the **temporary ingredient-overlap baseline** with TF-IDF + cosine similarity (or chosen recommendation algorithm).
- Quantify accuracy/precision, ingredient coverage, and response time.

## What Avery should do
- Implement photo-to-ingredient recognition and connect it to the existing uploaded file widget.
- Test detection accuracy on a clearly documented set of ingredient photos.

## Before the final submission
- Swap in the full dataset; manually inspect normalization failures.
- Ensure each group member documents code contributions and cite the real dataset in the report.
- Evaluate results and capture screenshots/demo video for the 6-minute presentation.
- Be honest about image recognition and recommenders that aren't yet implemented.
