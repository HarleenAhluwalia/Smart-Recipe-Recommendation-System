# Smart Recipe Recommendation System

## System Requirements

Our project uses Python 3.11 and can run on Windows or macOS. We used Python as our programming language, Pandas for processing recipe data, Streamlit for creating the application, and Pytest for testing.

## Installation Instructions

First, download and unzip the project folder. Next, open the terminal and go to the project folder. Make sure Python is installed on your computer. To install the required libraries, run the following command:

`python -m pip install -r requirements.txt`

## Running the Application

Once the libraries are installed, run the following command in the terminal:

`python -m streamlit run app.py`

The application should automatically open in your web browser. If it does not open, go to `http://localhost:8501`.

Users can enter their available ingredients, select a cuisine, and view recommended recipes.

## Testing

To test our project, we used Pytest to check if the ingredient preprocessing functions work correctly. To run the test cases, enter the following command in the terminal:

`python -m pytest -v`

The terminal will show whether the tests passed or failed.

## Login Credentials

No login or account is required to use our application.