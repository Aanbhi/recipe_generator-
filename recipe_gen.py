import tkinter as tk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk
import io
import threading

# Spoonacular API setup (Replace 'YOUR_API_KEY' with your actual key)
API_KEY = "c25f33a039f84132a0616d6737338feb"
BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"


# Function to get recipes
def get_recipes(ingredients, diet=None, cuisine=None):
    params = {
        "apiKey": API_KEY,
        "includeIngredients": ingredients,
        "diet": diet,
        "cuisine": cuisine,
        "number": 10,  # Fetch 10 recipes
        "addRecipeInformation": True,  # Include detailed recipe information
        "instructionsRequired": True  # Ensure recipes have instructions
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        recipes = data.get("results", [])
        return recipes
    else:
        messagebox.showerror("Error", "Failed to fetch recipes!")
        return []


# Function to load images asynchronously
def load_image_async(img_url, label):

    def load():
        try:
            img_data = requests.get(img_url).content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((200, 200))  # Size to fit the card
            img = ImageTk.PhotoImage(img)
            label.config(image=img)
            label.image = img
        except Exception as e:
            print("Image load failed:", e)

    threading.Thread(target=load).start()


# Function to display recipes in the GUI
def display_recipes(recipes):
    # Clear previous results
    for widget in results_container.winfo_children():
        widget.destroy()

    if not recipes:
        no_recipes_label = tk.Label(results_container,
                                    text="No recipes found.",
                                    font=("Helvetica", 14),
                                    bg="#F2E0C9",
                                    fg="#8B4513")
        no_recipes_label.pack(pady=20)
        return

    for recipe in recipes[:5]:  # Limit to 5 results for better readability
        recipe_frame = tk.Frame(results_container,
                                bd=2,
                                relief="solid",
                                padx=10,
                                pady=10,
                                bg="#F2E0C9",
                                width=400)
        recipe_frame.pack(padx=10, pady=10, side="top", fill="x", anchor="w")

        # Recipe image
        img_url = recipe.get("image", "")
        img_label = tk.Label(recipe_frame, bg="#F2E0C9")
        img_label.pack(side="left", padx=10)
        if img_url:
            load_image_async(img_url, img_label)

        # Recipe title and description
        title_frame = tk.Frame(recipe_frame, bg="#F2E0C9")
        title_frame.pack(side="left", fill="both", expand=True)

        title = tk.Label(title_frame,
                         text=recipe["title"],
                         font=("Helvetica", 16, "bold"),
                         bg="#F2E0C9",
                         fg="#8B4513")
        title.pack(anchor="w", pady=5)

        # Preparation time
        details = f"Prep Time: {recipe.get('readyInMinutes', 'N/A')} minutes"
        details_label = tk.Label(title_frame,
                                 text=details,
                                 font=("Helvetica", 12),
                                 bg="#F2E0C9",
                                 fg="#8B4513")
        details_label.pack(anchor="w", pady=5)

        # Instructions
        instructions = recipe.get("analyzedInstructions", [])
        if instructions:
            steps = "\n".join([
                f"{step['number']}. {step['step']}"
                for step in instructions[0].get("steps", [])[:3]
            ])  # Limit to first 3 steps
            instructions_label = tk.Label(title_frame,
                                          text=f"Instructions:\n{steps}",
                                          justify="left",
                                          wraplength=250,
                                          bg="#F2E0C9",
                                          fg="#8B4513")
            instructions_label.pack(anchor="w", pady=5)
        else:
            instructions_label = tk.Label(title_frame,
                                          text="Instructions: Not available.",
                                          bg="#F2E0C9",
                                          fg="#8B4513")
            instructions_label.pack(anchor="w")

        # Like button (interactive)
        like_button = tk.Button(title_frame,
                                text="Like",
                                command=lambda: like_recipe(recipe["title"]),
                                bg="#8B4513",
                                fg="white",
                                font=("Helvetica", 12))
        like_button.pack(side="right", pady=10)

    # Update the canvas scroll region
    results_container.update_idletasks()
    results_canvas.config(scrollregion=results_canvas.bbox("all"))


# Like Recipe function
def like_recipe(recipe_name):
    messagebox.showinfo("Recipe Liked", f"You liked the recipe: {recipe_name}")


# Function to add ingredients to the list
def add_ingredient():
    ingredient = ingredient_entry.get().strip()
    if ingredient:
        if ingredient not in ingredient_listbox.get(0, tk.END):
            ingredient_listbox.insert(tk.END, ingredient)
            ingredient_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Duplicate Ingredient",
                                "This ingredient is already added.")
    else:
        messagebox.showwarning("Input Error", "Please enter an ingredient.")


# Function to remove selected ingredient from the list
def remove_ingredient():
    selected_items = ingredient_listbox.curselection()
    if selected_items:
        for item in reversed(selected_items):  # Remove selected items
            ingredient_listbox.delete(item)
    else:
        messagebox.showwarning("Selection Error",
                               "Please select an ingredient to remove.")


# Function to get all ingredients from the list
def get_all_ingredients():
    return ",".join(ingredient_listbox.get(0, tk.END))


# Function to fetch recipes based on the ingredients
def fetch_recipes():
    ingredients = get_all_ingredients()
    if not ingredients:
        messagebox.showwarning("Input Error",
                               "Please add at least one ingredient.")
        return

    diet = diet_combo.get()
    cuisine = cuisine_combo.get()

    # Show a loading message while fetching recipes
    loading_label = tk.Label(results_frame,
                             text="Fetching recipes...",
                             font=("Helvetica", 14),
                             bg="#F2E0C9",
                             fg="#8B4513")
    loading_label.pack(pady=20)

    recipes = get_recipes(ingredients, diet, cuisine)
    loading_label.pack_forget()  # Remove the loading message
    display_recipes(recipes)


# GUI Setup with Tkinter
root = tk.Tk()
root.title("AI-Powered Recipe Generator")
root.geometry("900x700")
root.config(bg="#F2E0C9")  # Plaster color

# Title Label
title_label = tk.Label(root,
                       text="AI-Powered Recipe Generator",
                       font=("Helvetica", 24, "bold"),
                       bg="#F2E0C9",
                       fg="#8B4513")
title_label.pack(pady=10)

# Input Section
input_frame = tk.Frame(root, pady=10, bg="#F2E0C9")
input_frame.pack(padx=10, pady=10, fill="x")

ingredient_label = tk.Label(input_frame,
                            text="Enter Ingredients:",
                            bg="#F2E0C9",
                            fg="#8B4513",
                            font=("Helvetica", 14))
ingredient_label.pack(anchor="w")

ingredient_entry = tk.Entry(input_frame,
                            width=50,
                            font=("Helvetica", 14),
                            bd=2)
ingredient_entry.pack(anchor="w", pady=5)

# Add Ingredient Button
add_button = tk.Button(input_frame,
                       text="Add Ingredient",
                       command=add_ingredient,
                       bg="white",
                       fg="#8B4513",
                       font=("Helvetica", 12))
add_button.pack(side="left", padx=5)

# Remove Ingredient Button
remove_button = tk.Button(input_frame,
                          text="Remove Selected",
                          command=remove_ingredient,
                          bg="white",
                          fg="#8B4513",
                          font=("Helvetica", 12))
remove_button.pack(side="left", padx=5)

ingredient_listbox = tk.Listbox(input_frame,
                                height=5,
                                bg="white",
                                fg="#8B4513",
                                font=("Helvetica", 12),
                                bd=2)
ingredient_listbox.pack(anchor="w", pady=5)

# Diet and Cuisine Options
diet_label = tk.Label(input_frame,
                      text="Select Diet (optional):",
                      bg="#F2E0C9",
                      fg="#8B4513",
                      font=("Helvetica", 14))
diet_label.pack(anchor="w")

diet_combo = ttk.Combobox(
    input_frame,
    values=["", "Vegan", "Vegetarian", "Gluten Free", "Keto"],
    font=("Helvetica", 12))
diet_combo.pack(anchor="w", pady=5)

cuisine_label = tk.Label(input_frame,
                         text="Select Cuisine (optional):",
                         bg="#F2E0C9",
                         fg="#8B4513",
                         font=("Helvetica", 14))
cuisine_label.pack(anchor="w")

cuisine_combo = ttk.Combobox(
    input_frame,
    values=["", "Italian", "Chinese", "Indian", "Mexican"],
    font=("Helvetica", 12))
cuisine_combo.pack(anchor="w", pady=5)

# Fetch Recipes Button
fetch_button = tk.Button(input_frame,
                         text="Get Recipes",
                         command=fetch_recipes,
                         bg="#8B4513",
                         fg="white",
                         font=("Helvetica", 14))
fetch_button.pack(pady=10)

# Scrollable Result Section
results_frame = tk.Frame(root, bg="#F2E0C9")
results_frame.pack(padx=10, pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(results_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

results_canvas = tk.Canvas(results_frame,
                           yscrollcommand=scrollbar.set,
                           bg="#F2E0C9")
results_canvas.pack(side="left", fill="both", expand=True)

scrollbar.config(command=results_canvas.yview)

# Create a frame inside the canvas to hold results
results_container = tk.Frame(results_canvas, bg="#F2E0C9")
results_canvas.create_window((0, 0), window=results_container, anchor="nw")

# Run the application
root.mainloop()
