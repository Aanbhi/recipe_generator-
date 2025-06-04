# main.py
import tkinter as tk
from tkinter import ttk
from api import get_recipes
from gui_utils import display_recipes
from events import like_recipe, add_ingredient, remove_ingredient, get_all_ingredients

root = tk.Tk()
root.title("AI-Powered Recipe Generator")
root.geometry("900x700")
root.config(bg="#F2E0C9")

title_label = tk.Label(root, text="AI-Powered Recipe Generator", font=("Helvetica", 24, "bold"),
                       bg="#F2E0C9", fg="#8B4513")
title_label.pack(pady=10)

input_frame = tk.Frame(root, pady=10, bg="#F2E0C9")
input_frame.pack(padx=10, pady=10, fill="x")

ingredient_label = tk.Label(input_frame, text="Enter Ingredients:", bg="#F2E0C9",
                            fg="#8B4513", font=("Helvetica", 14))
ingredient_label.pack(anchor="w")

ingredient_entry = tk.Entry(input_frame, width=50, font=("Helvetica", 14), bd=2)
ingredient_entry.pack(anchor="w", pady=5)

ingredient_listbox = tk.Listbox(input_frame, height=5, bg="white", fg="#8B4513",
                                font=("Helvetica", 12), bd=2)
ingredient_listbox.pack(anchor="w", pady=5)

tk.Button(input_frame, text="Add Ingredient", command=lambda: add_ingredient(ingredient_entry, ingredient_listbox),
          bg="white", fg="#8B4513", font=("Helvetica", 12)).pack(side="left", padx=5)

tk.Button(input_frame, text="Remove Selected", command=lambda: remove_ingredient(ingredient_listbox),
          bg="white", fg="#8B4513", font=("Helvetica", 12)).pack(side="left", padx=5)

diet_label = tk.Label(input_frame, text="Select Diet (optional):", bg="#F2E0C9",
                      fg="#8B4513", font=("Helvetica", 14))
diet_label.pack(anchor="w")

diet_combo = ttk.Combobox(input_frame, values=["", "Vegan", "Vegetarian", "Gluten Free", "Keto"],
                          font=("Helvetica", 12))
diet_combo.pack(anchor="w", pady=5)

cuisine_label = tk.Label(input_frame, text="Select Cuisine (optional):", bg="#F2E0C9",
                         fg="#8B4513", font=("Helvetica", 14))
cuisine_label.pack(anchor="w")

cuisine_combo = ttk.Combobox(input_frame, values=["", "Italian", "Chinese", "Indian", "Mexican"],
                             font=("Helvetica", 12))
cuisine_combo.pack(anchor="w", pady=5)

results_frame = tk.Frame(root, bg="#F2E0C9")
results_frame.pack(padx=10, pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(results_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

results_canvas = tk.Canvas(results_frame, yscrollcommand=scrollbar.set, bg="#F2E0C9")
results_canvas.pack(side="left", fill="both", expand=True)
scrollbar.config(command=results_canvas.yview)

results_container = tk.Frame(results_canvas, bg="#F2E0C9")
results_canvas.create_window((0, 0), window=results_container, anchor="nw")

def fetch_recipes():
    ingredients = get_all_ingredients(ingredient_listbox)
    if not ingredients:
        messagebox.showwarning("Input Error", "Please add at least one ingredient.")
        return

    loading_label = tk.Label(results_frame, text="Fetching recipes...",
                             font=("Helvetica", 14), bg="#F2E0C9", fg="#8B4513")
    loading_label.pack(pady=20)

    diet = diet_combo.get()
    cuisine = cuisine_combo.get()

    recipes = get_recipes(ingredients, diet, cuisine)
    loading_label.destroy()
    display_recipes(recipes, results_container, results_canvas, like_recipe)

tk.Button(input_frame, text="Get Recipes", command=fetch_recipes,
          bg="#8B4513", fg="white", font=("Helvetica", 14)).pack(pady=10)

root.mainloop()
