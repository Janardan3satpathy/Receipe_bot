import json
import random

def generate_500_recipes():
    # Basic lists to mix and match
    proteins = ["Chicken", "Egg", "Tofu", "Beef", "Paneer", "Fish"]
    vegetables = ["Onion", "Tomato", "Spinach", "Potato", "Carrot", "Peas", "Bell Pepper"]
    carbs = ["Rice", "Pasta", "Bread", "Noodles", "Quinoa"]
    spices = ["Salt", "Pepper", "Cumin", "Turmeric", "Garlic", "Ginger", "Soy Sauce"]
    methods = ["Fry", "Boil", "Bake", "Grill", "Sauté", "Steam"]

    dataset = []

    print("Generating 500 recipes...")

    for i in range(500):
        # Randomly select ingredients
        p = random.choice(proteins)
        v = random.choice(vegetables)
        c = random.choice(carbs)
        s = random.choice(spices)
        m = random.choice(methods)
        
        # Create input string
        ingredients = f"{p}, {v}, {c}, {s}"
        
        # Create a synthetic recipe output
        recipe_name = f"{m}ed {p} with {v} and {c}"
        steps = f"1. Prepare the {p} and {v}. 2. Heat pan and add {s}. 3. {m} the {p} for 10 mins. 4. Add {v} and serve with {c}."
        
        entry = {
            "ingredients": ingredients,
            "recipe": f"{recipe_name}: {steps}"
        }
        dataset.append(entry)

    # Save to file
    with open("recipes_500.json", "w") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"✅ Successfully created 'recipes_500.json' with {len(dataset)} examples.")

if __name__ == "__main__":
    generate_500_recipes()