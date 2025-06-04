# gui_utils.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import requests
import io

def load_image_async(img_url, label):
    def load():
        try:
            img_data = requests.get(img_url).content
            img = Image.open(io.BytesIO(img_data)).resize((200, 200))
            img = ImageTk.PhotoImage(img)
            label.config(image=img)
            label.image = img
        except Exception as e:
            print("Image load failed:", e)
    threading.Thread(target=load).start()

def display_recipes(recipes, results_container, results_canvas, like_callback):
    for widget in results_container.winfo_children():
        widget.destroy()

    if not recipes:
        tk.Label(results_container, text="No recipes found.", font=("Helvetica", 14),
                 bg="#F2E0C9", fg="#8B4513").pack(pady=20)
        return

    for recipe in recipes[:5]:
        recipe_frame = tk.Frame(results_container, bd=2, relief="solid", padx=10, pady=10, bg="#F2E0C9")
        recipe_frame.pack(padx=10, pady=10, side="top", fill="x", anchor="w")

        img_url = recipe.get("image", "")
        img_label = tk.Label(recipe_frame, bg="#F2E0C9")
        img_label.pack(side="left", padx=10)
        if img_url:
            load_image_async(img_url, img_label)

        title_frame = tk.Frame(recipe_frame, bg="#F2E0C9")
        title_frame.pack(side="left", fill="both", expand=True)

        tk.Label(title_frame, text=recipe["title"], font=("Helvetica", 16, "bold"),
                 bg="#F2E0C9", fg="#8B4513").pack(anchor="w", pady=5)

        details = f"Prep Time: {recipe.get('readyInMinutes', 'N/A')} minutes"
        tk.Label(title_frame, text=details, font=("Helvetica", 12),
                 bg="#F2E0C9", fg="#8B4513").pack(anchor="w", pady=5)

        instructions = recipe.get("analyzedInstructions", [])
        if instructions:
            steps = "\n".join([f"{step['number']}. {step['step']}"
                               for step in instructions[0].get("steps", [])[:3]])
            tk.Label(title_frame, text=f"Instructions:\n{steps}", justify="left",
                     wraplength=250, bg="#F2E0C9", fg="#8B4513").pack(anchor="w", pady=5)
        else:
            tk.Label(title_frame, text="Instructions: Not available.",
                     bg="#F2E0C9", fg="#8B4513").pack(anchor="w")

        tk.Button(title_frame, text="Like", command=lambda r=recipe["title"]: like_callback(r),
                  bg="#8B4513", fg="white", font=("Helvetica", 12)).pack(side="right", pady=10)

    results_container.update_idletasks()
    results_canvas.config(scrollregion=results_canvas.bbox("all"))
