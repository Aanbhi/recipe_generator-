🍽️ AI-Powered Recipe Generator (Tkinter GUI)

This is a desktop application that uses the Spoonacular API to generate delicious recipes based on ingredients you have. Built with Python's Tkinter for the user interface, it allows users to input ingredients, choose optional dietary and cuisine preferences, and receive visually appealing recipes complete with steps, prep time, and images.


🌟 Features

1. Search recipes using your available ingredients

2. Filter results by diet (e.g., Vegan, Keto) and cuisine (e.g., Italian, Indian)

3. Scrollable, card-style recipe display with:

a) Title

b) Image

c) Prep time

d) Cooking instructions

4. "Like" button for user interaction (demo popup)

5. Clean and aesthetic UI styled with a warm, neutral color palette

6. Async image loading for better performance


📦 Requirements

Install the dependencies with:

pip install requests pillow

Note: tkinter is included with most Python installations.


🚀 How to Run

1. Clone the repository:

git clone https://github.com/Aanbhi/recipe_generator.git

cd recipe_gen

2. Replace the placeholder API key in the code:

Edit the following line in the script:

API_KEY = "YOUR_API_KEY"  # Replace with your Spoonacular API key

3. Run the application:

python recipe_gen.py

📂 Project Structure


FORMAT - 1


recipe_app/


├── main.py                 # Entry point for GUI

├── api.py                 # Spoonacular API functions

├── gui_utils.py           # GUI helper functions (image loading, recipe display)

├── events.py              # Event handlers (button clicks, interactions)

└── config.py              # Configuration like API keys and constants


FORMAT - 2


├── recipe_gen.py    # Main GUI application code



├── README.md        # Project documentation

├── requirements.txt    #Install the dependencies

📸 Preview

A sample GUI with search and recipe cards.


🔑 Get Your API Key

You’ll need a Spoonacular API key to use this app. Sign up and get it here:

👉 https://spoonacular.com/food-api


🛠️ Future Improvements

1. Add favorites system with local storage or database

2. Export/sharing options for recipes

3. Improve error handling and offline caching


👨‍💻 Author

Made with 💡 by ANBHI THAKUR
