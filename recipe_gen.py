recipes = [
    {
        "name": "Pasta Primavera",
        "ingredients": {"pasta": 100, "vegetables": 200, "olive oil": 10, "garlic": 5},
        "cuisine": "Italian",
        "diet": {"vegetarian"},
        "description": "A fresh pasta dish loaded with seasonal vegetables.",
        "serving_size": 2,
        "cooking_time": 30,  # in minutes
        "nutrition": {"calories": 400}
    },
    {
        "name": "Omelette",
        "ingredients": {"eggs": 3, "cheese": 50, "vegetables": 100},
        "cuisine": "Breakfast",
        "diet": {"vegetarian", "gluten-free"},
        "description": "A classic omelette filled with cheese and veggies.",
        "serving_size": 1,
        "cooking_time": 15,
        "nutrition": {"calories": 300}
    },
    {
        "name": "Vegetable Stir Fry",
        "ingredients": {"vegetables": 300, "soy sauce": 20, "olive oil": 10},
        "cuisine": "Chinese",
        "diet": {"vegan", "gluten-free", "vegetarian"},
        "description": "Quick and easy stir-fried vegetables.",
        "serving_size": 2,
        "cooking_time": 20,
        "nutrition": {"calories": 250}
    },
    {
        "name": "Chili",
        "ingredients": {"beans": 200, "tomato": 150, "ground meat": 100, "spices": 10},
        "cuisine": "American",
        "diet": {"gluten-free"},
        "description": "A hearty and spicy chili dish.",
        "serving_size": 4,
        "cooking_time": 40,
        "nutrition": {"calories": 500}
    },
    {
        "name": "Tacos",
        "ingredients": {"tortillas": 4, "beans": 200, "cheese": 100, "vegetables": 150},
        "cuisine": "Mexican",
        "diet": {"vegetarian"},
        "description": "Delicious tacos filled with beans and cheese.",
        "serving_size": 2,
        "cooking_time": 25,
        "nutrition": {"calories": 350}
    },
    {
        "name": "Guacamole",
        "ingredients": {"avocado": 2, "tomato": 100, "onion": 50, "lime": 1},
        "cuisine": "Mexican",
        "diet": {"vegan", "gluten-free"},
        "description": "A creamy avocado dip perfect for snacks.",
        "serving_size": 4,
        "cooking_time": 10,
        "nutrition": {"calories": 200}
    },
]

def adjust_ingredients(recipe, servings):
    adjusted_ingredients = {}
    for ingredient, amount in recipe["ingredients"].items():
        adjusted_ingredients[ingredient] = amount * (servings / recipe["serving_size"])
    return adjusted_ingredients

def suggest_recipes(available_ingredients, preferred_cuisines, dietary_restrictions, servings):
    available_set = set(available_ingredients)
    suggested_recipes = []

    for recipe in recipes:
        # Check if all ingredients are available
        if recipe["ingredients"].keys() <= available_set:
            # Check for dietary restrictions
            if not recipe["diet"].isdisjoint(dietary_restrictions) or not dietary_restrictions:
                # Check for preferred cuisines
                if recipe["cuisine"] in preferred_cuisines or not preferred_cuisines:
                    adjusted_ingredients = adjust_ingredients(recipe, servings)
                    suggested_recipes.append({
                        "name": recipe["name"],
                        "description": recipe["description"],
                        "adjusted_ingredients": adjusted_ingredients,
                        "cuisine": recipe["cuisine"],
                        "diet": recipe["diet"],
                        "cooking_time": recipe["cooking_time"],
                        "nutrition": recipe["nutrition"]
                    })

    return suggested_recipes

def main():
    user_input = input("Enter up to 10 available ingredients, separated by commas: ")
    available_ingredients = [ingredient.strip() for ingredient in user_input.split(",")]

    cuisines_input = input("Enter your preferred cuisines (comma-separated), or leave blank for all: ")
    preferred_cuisines = [cuisine.strip() for cuisine in cuisines_input.split(",")] if cuisines_input else []

    dietary_input = input("Enter your dietary restrictions (comma-separated), or leave blank for none: ")
    dietary_restrictions = {diet.strip() for diet in dietary_input.split(",")} if dietary_input else set()

    servings_input = input("Enter the number of servings you want: ")
    servings = int(servings_input)

    suggestions = suggest_recipes(available_ingredients, preferred_cuisines, dietary_restrictions, servings)

    if suggestions:
        print("\nYou can make the following recipes:")
        for recipe in suggestions:
            print(f"\nRecipe: {recipe['name']}")
            print(f"Cuisine: {recipe['cuisine']}")
            print(f"Description: {recipe['description']}")
            print(f"Cooking time: {recipe['cooking_time']} minutes")
            print("Adjusted Ingredients:")
            for ingredient, amount in recipe['adjusted_ingredients'].items():
                print(f"- {ingredient}: {amount:.2f}")
            print(f"Diet: {', '.join(recipe['diet'])}")
            print(f"Nutritional Info: {recipe['nutrition']['calories']} calories")
    else:
        print("No recipes can be made with the given ingredients and preferences.")

if __name__ == "__main__":
    main()

# output 1
# pasta, vegetables, olive oil, garlic,eggs, cheese,soy sauce,beans, tomato, ground meat
# Italian, Chinese, Breakfast 
# vegetarian
# 3 
