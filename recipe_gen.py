import tkinter as tk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk
import io

# Spoonacular API setup (Replace 'YOUR_API_KEY' with your actual key)
API_KEY = "c25f33a039f84132a0616d6737338feb"
BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"

# Function to call the Spoonacular API and fetch recipes
def get_recipes(ingredients, diet=None, cuisine=None):
    params = {
        "apiKey": API_KEY,
        "includeIngredients": ingredients,
        "diet": diet,
        "cuisine": cuisine,
        "number": 3,  # Fetch 3 recipes
        "addRecipeInformation": True
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        messagebox.showerror("Error", "Failed to fetch recipes!")
        return []

# Function to display recipe results
def display_recipes(recipes):
    for widget in result_frame.winfo_children():
        widget.destroy()  # Clear previous results

    if not recipes:
        messagebox.showinfo("No Recipes Found", "No matching recipes found!")
        return

    for recipe in recipes:
        recipe_frame = tk.Frame(result_frame, bd=2, relief="groove", padx=10, pady=5)
        recipe_frame.pack(fill="x", padx=5, pady=5)

        title = tk.Label(recipe_frame, text=recipe["title"], font=("Arial", 14, "bold"))
        title.pack(anchor="w")

        img_url = recipe["image"]
        try:
            img_data = requests.get(img_url).content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)

            img_label = tk.Label(recipe_frame, image=img)
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.pack(side="left", padx=10)
        except Exception as e:
            print("Image load failed:", e)

        details = "Servings: {recipe.get('servings', 'N/A')} | Time: {recipe.get('readyInMinutes', 'N/A')} mins"
        details_label = tk.Label(recipe_frame, text=details)
        details_label.pack(anchor="w")

        instructions = tk.Label(recipe_frame, text=recipe.get("sourceUrl", ""), fg="blue", cursor="hand2")
        instructions.pack(anchor="w")
        instructions.bind("<Button-1>", lambda e, url=recipe["sourceUrl"]: open_url(url))

# Open recipe URL in browser
def open_url(url):
    import webbrowser
    webbrowser.open(url)

# Function to handle user input and fetch recipes
def fetch_recipes():
    ingredients = ingredient_entry.get()
    if not ingredients:
        messagebox.showwarning("Input Error", "Please enter at least one ingredient.")
        return

    diet = diet_combo.get()
    cuisine = cuisine_combo.get()
    recipes = get_recipes(ingredients, diet, cuisine)
    display_recipes(recipes)

# GUI Setup with Tkinter
root = tk.Tk()
root.title("AI-Powered Recipe Generator")
root.geometry("600x600")

# Input Section
input_frame = tk.Frame(root, pady=10)
input_frame.pack(padx=10, pady=10, fill="x")

ingredient_label = tk.Label(input_frame, text="Enter Ingredients (comma-separated):")
ingredient_label.pack(anchor="w")

ingredient_entry = tk.Entry(input_frame, width=50)
ingredient_entry.pack(anchor="w", pady=5)

diet_label = tk.Label(input_frame, text="Select Diet (optional):")
diet_label.pack(anchor="w")

diet_combo = ttk.Combobox(input_frame, values=["", "Vegan", "Vegetarian", "Gluten Free", "Keto"])
diet_combo.pack(anchor="w", pady=5)

cuisine_label = tk.Label(input_frame, text="Select Cuisine (optional):")
cuisine_label.pack(anchor="w")

cuisine_combo = ttk.Combobox(input_frame, values=["", "Italian", "Chinese", "Indian", "Mexican"])
cuisine_combo.pack(anchor="w", pady=5)

fetch_button = tk.Button(input_frame, text="Get Recipes", command=fetch_recipes)
fetch_button.pack(pady=10)

# Result Section
result_frame = tk.Frame(root, pady=10)
result_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Run the application
root.mainloop()
