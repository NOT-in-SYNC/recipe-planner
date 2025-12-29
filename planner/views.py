from django.shortcuts import render, redirect
from .models import Recipe, Ingredient

# --- VIEW 1: The Home Page (List of Recipes) ---
def home(request):
    # Fetch all recipes from the database
    recipes = Recipe.objects.all()
    # Send them to the HTML file
    return render(request, 'planner/home.html', {'recipes': recipes})

# --- VIEW 2: The Add Recipe Page (Form Logic) ---
def add_recipe(request):
    if request.method == "POST":
        # 1. Get data from the form
        title = request.POST.get('title')
        desc = request.POST.get('description')
        time = request.POST.get('prep_time')
        ingredients_text = request.POST.get('ingredients')

        # 2. Create the Recipe object first
        new_recipe = Recipe.objects.create(
            title=title,
            description=desc,
            prep_time_minutes=time
        )

        # 3. Process the Ingredients text
        # We split the text by "newlines" to get a list of lines
        lines = ingredients_text.split('\n')
        
        for line in lines:
            line = line.strip() # Remove empty spaces
            if line: # Only process if line is not empty
                # We expect format: "Quantity - Name"
                parts = line.split('-', 1) 
                
                if len(parts) == 2:
                    qty = parts[0].strip()
                    name = parts[1].strip()
                else:
                    # Fallback if user forgot the dash
                    qty = "1 unit"
                    name = line
                
                # Save Ingredient linked to the new recipe
                Ingredient.objects.create(
                    recipe=new_recipe,
                    quantity=qty,
                    name=name
                )

        # 4. Done! Go back home
        return redirect('home')

    return render(request, 'planner/add_recipe.html')