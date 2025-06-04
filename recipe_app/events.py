# events.py
from tkinter import messagebox

def like_recipe(recipe_name):
    messagebox.showinfo("Recipe Liked", f"You liked the recipe: {recipe_name}")

def add_ingredient(ingredient_entry, ingredient_listbox):
    ingredient = ingredient_entry.get().strip()
    if ingredient:
        if ingredient not in ingredient_listbox.get(0, "end"):
            ingredient_listbox.insert("end", ingredient)
            ingredient_entry.delete(0, "end")
        else:
            messagebox.showinfo("Duplicate Ingredient", "This ingredient is already added.")
    else:
        messagebox.showwarning("Input Error", "Please enter an ingredient.")

def remove_ingredient(ingredient_listbox):
    selected_items = ingredient_listbox.curselection()
    if selected_items:
        for item in reversed(selected_items):
            ingredient_listbox.delete(item)
    else:
        messagebox.showwarning("Selection Error", "Please select an ingredient to remove.")

def get_all_ingredients(ingredient_listbox):
    return ",".join(ingredient_listbox.get(0, "end"))
