# Smart Recipe Recommendation System

## System Requirements

Our project uses Python 3.11 and can run on Windows or macOS. We used Python to build our application, Pandas to clean and organize recipe data, Streamlit to create the user interface, and Pytest to test our code. We also used Pillow and the Anthropic API (Claude AI) for ingredient photo recognition.

An internet connection and an Anthropic API key are needed for the photo recognition feature.

## Installation Instructions

First, download and unzip the project folder. Then, open the terminal and go to the project folder. Make sure Python is installed on your computer.

To install the required libraries, enter this command:

`python -m pip install -r requirements.txt`

## API Key Setup

Our photo recognition feature uses the Anthropic API. Users can still type ingredients and get recipe recommendations without an API key.

To set up the API key:

1. Open the project folder.
2. Create a folder named `.streamlit` if it does not already exist.
3. Inside that folder, create a file named `secrets.toml`.
4. Add the following line and replace the example with your API key:

`ANTHROPIC_API_KEY = "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"`

## Running the Application

After installing the libraries, run the following command in the terminal:

`python -m streamlit run app.py`

The application should open in your browser. If it does not open automatically, go to http://localhost:8501.

Users can enter their ingredients, upload a photo, or take a picture using their camera. They can also select a cuisine and get recipe recommendations.

When a photo is uploaded, the system uses Claude AI to identify the ingredients. Users can check and edit the detected ingredients before getting recipe recommendations.

## Image Recognition

Our project uses Anthropic's Claude AI to recognize ingredients from pictures. The system identifies ingredients from an uploaded photo and compares them with the ingredients in our recipe dataset.

We tested this feature by uploading ingredient photos and checking if the AI identified the ingredients correctly.

The image recognition code is in `image_recognition.py`.

## Testing

We used Pytest to check if our ingredient preprocessing functions work correctly.

To run the tests, enter:

`python -m pytest -v`

The terminal will show which tests passed or failed.

**Test Results:** We ran our tests, and both tests passed (2 passed).

## Login Credentials

No login or account is required to use our application. An Anthropic API key is only needed for the ingredient photo feature.


## Credits

- Ingredient recognition uses Anthropic's Claude Opus 5.5 vision model through the Anthropic API (https://www.anthropic.com).
- Pillow was used to resize and prepare images.
