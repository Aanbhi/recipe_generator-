# api.py
import requests
from tkinter import messagebox
from config import API_KEY, BASE_URL

def get_recipes(ingredients, diet=None, cuisine=None):
    params = {
        "apiKey": API_KEY,
        "includeIngredients": ingredients,
        "diet": diet,
        "cuisine": cuisine,
        "number": 10,
        "addRecipeInformation": True,
        "instructionsRequired": True
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        messagebox.showerror("Error", "Failed to fetch recipes!")
        return []
