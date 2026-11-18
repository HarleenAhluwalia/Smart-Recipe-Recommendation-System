# Smart Recipe Recommendation System

## System Requirements

Our project uses Python 3.11 and can run on Windows or macOS. We used Python as our programming language, Pandas for processing recipe data, Streamlit for creating the application, and Pytest for testing. For the ingredient photo feature, we used the Anthropic API (Claude) for image recognition and Pillow for preparing images. The photo feature needs an internet connection and an Anthropic API key.

## Installation Instructions

First, download and unzip the project folder. Next, open the terminal and go to the project folder. Make sure Python is installed on your computer. To install the required libraries, run the following command:

`python -m pip install -r requirements.txt`

## API Key Setup

The ingredient photo feature uses an Anthropic API key. Typing ingredients works without a key.

1. Create an API key at https://console.anthropic.com.
2. In the project folder, create a folder named `.streamlit` and a file inside it named `secrets.toml`.
3. Add this line to `secrets.toml`, replacing the example with your key:

`ANTHROPIC_API_KEY = "sk-ant-your-key-here"`

This file is listed in `.gitignore` so the key is never uploaded to GitHub. Do not share your key or commit it.

## Running the Application

Once the libraries are installed, run the following command in the terminal:

`python -m streamlit run app.py`

The application should automatically open in your web browser. If it does not open, go to `http://localhost:8501`.

Users can type their available ingredients, upload a photo or take a picture with their camera, select a cuisine, and view recommended recipes. When a photo is added, the ingredients found in it are shown in a list that the user can edit before searching. Ingredients from the photo and typed ingredients are combined for the search.

## Image Recognition

When a user adds a photo, our program resizes it and sends it to Anthropic's Claude Opus 5.5 vision model along with a list of ingredient names from our recipe dataset. Claude returns the ingredients it can see and how confident it is in each one (high, medium, or low). We only keep ingredients that are in our dataset and that are at least medium confidence, so the results can be matched to recipes. Seasonings and liquids such as salt, pepper, and oil are left out because they cannot be reliably identified from a photo.

This code is in `image_recognition.py`. Each photo is only sent once, even if the user changes other settings, to avoid repeated API costs.

### Evaluating Accuracy

We measured image recognition accuracy using our own labeled photos. The photos and the correct ingredients for each one are in `data/vision_test/`, listed in `labels.csv`. To run the evaluation, enter the following command in the terminal:

`python evaluate_vision.py`

This sends each photo to Claude once, saves the results, and prints the precision (how many detected ingredients were correct), recall (how many of the real ingredients were found), and F1 score. To score the saved results again without using the API, run:

`python evaluate_vision.py --rescore`

**Results:** _To be added after testing._


## Testing

To test our project, we used Pytest to check if the ingredient preprocessing functions work correctly. To run the test cases, enter the following command in the terminal:

`python -m pytest -v`

The terminal will show whether the tests passed or failed.

## Login Credentials

No login or account is required to use our application. An Anthropic API key is only needed for the ingredient photo feature (see API Key Setup).

## Credits

- Ingredient recognition uses Anthropic's Claude Opus 5.5 vision model through the Anthropic API (https://www.anthropic.com).
- Pillow was used to resize and prepare images.
