from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Recipe, Ingredient

# --- 1. THE TEMPLATE LIBRARY (Hardcoded Data) ---
# These act as the "Store" items. They are NOT in the database until clicked.
RECIPE_TEMPLATES = [
    {"id": 1, "title": "Classic Pancakes", "desc": "Fluffy breakfast staple.", "time": 20, "ingredients": ["200g - Flour", "2 - Eggs", "300ml - Milk", "1 tsp - Baking Powder"]},
    {"id": 2, "title": "Spaghetti Bolognese", "desc": "Italian classic with beef.", "time": 45, "ingredients": ["400g - Minced Beef", "500g - Spaghetti", "1 jar - Tomato Sauce", "1 - Onion"]},
    {"id": 3, "title": "Chicken Caesar Salad", "desc": "Fresh and crunchy lunch.", "time": 15, "ingredients": ["2 - Chicken Breasts", "1 head - Lettuce", "50g - Parmesan", "100ml - Caesar Dressing"]},
    {"id": 4, "title": "Vegetable Stir Fry", "desc": "Quick healthy dinner.", "time": 20, "ingredients": ["1 - Broccoli Head", "2 - Carrots", "1 tbsp - Soy Sauce", "200g - Rice"]},
    {"id": 5, "title": "Grilled Cheese Sandwich", "desc": "Comfort food classic.", "time": 10, "ingredients": ["4 slices - Bread", "4 slices - Cheddar Cheese", "2 tbsp - Butter"]},
    {"id": 6, "title": "Tacos", "desc": "Mexican night favorite.", "time": 30, "ingredients": ["6 - Taco Shells", "300g - Ground Beef", "100g - Salsa", "100g - Shredded Cheese"]},
    {"id": 7, "title": "Omelet", "desc": "Protein packed breakfast.", "time": 10, "ingredients": ["3 - Eggs", "50g - Cheese", "1 handful - Spinach", "1 pinch - Salt"]},
    {"id": 8, "title": "Chicken Curry", "desc": "Spicy and creamy.", "time": 40, "ingredients": ["500g - Chicken", "1 jar - Curry Sauce", "200g - Rice", "1 - Naan Bread"]},
    {"id": 9, "title": "Tomato Soup", "desc": "Warm winter meal.", "time": 25, "ingredients": ["1kg - Tomatoes", "1 - Onion", "500ml - Veg Stock", "100ml - Cream"]},
    {"id": 10, "title": "Avocado Toast", "desc": "Trendy brunch.", "time": 5, "ingredients": ["2 slices - Sourdough", "1 - Avocado", "1 pinch - Chili Flakes", "1 squeeze - Lemon"]},
    {"id": 11, "title": "Beef Burger", "desc": "Homemade burger night.", "time": 25, "ingredients": ["2 - Burger Buns", "2 - Beef Patties", "1 - Tomato", "1 - Lettuce Leaf"]},
    {"id": 12, "title": "Fruit Salad", "desc": "Healthy dessert.", "time": 10, "ingredients": ["1 - Apple", "1 - Banana", "1 handful - Grapes", "1 - Orange"]},
    {"id": 13, "title": "Mac and Cheese", "desc": "Cheesy goodness.", "time": 20, "ingredients": ["300g - Macaroni", "200g - Cheddar", "500ml - Milk", "50g - Butter"]},
    {"id": 14, "title": "Tuna Salad", "desc": "Protein rich lunch.", "time": 10, "ingredients": ["1 can - Tuna", "2 tbsp - Mayo", "1 stick - Celery", "1 handful - Corn"]},
    {"id": 15, "title": "French Toast", "desc": "Sweet breakfast treat.", "time": 15, "ingredients": ["4 slices - Bread", "2 - Eggs", "1 tsp - Cinnamon", "1 tbsp - Sugar"]},
]

# --- 2. THE VIEWS ---

def home(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) | Q(ingredients__name__icontains=query)
        ).distinct()
    else:
        recipes = Recipe.objects.all()
    return render(request, 'planner/home.html', {'recipes': recipes})

def add_recipe(request):
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('description')
        time = request.POST.get('prep_time')
        ingredients_text = request.POST.get('ingredients')

        new_recipe = Recipe.objects.create(title=title, description=desc, prep_time_minutes=time)
        
        lines = ingredients_text.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('-', 1)
                if len(parts) == 2:
                    qty, name = parts[0].strip(), parts[1].strip()
                else:
                    qty, name = "1 unit", line
                Ingredient.objects.create(recipe=new_recipe, quantity=qty, name=name)
        
        return redirect('home')
    return render(request, 'planner/add_recipe.html')

# --- NEW VIEW: Show the Templates ---
def browse_templates(request):
    return render(request, 'planner/templates.html', {'templates': RECIPE_TEMPLATES})

# --- NEW VIEW: Logic to Copy Template to DB ---
def copy_template(request, template_id):
    # 1. Find the selected template dictionary
    template = next((t for t in RECIPE_TEMPLATES if t['id'] == template_id), None)
    
    if template:
        # 2. Create the Recipe in the Database
        new_recipe = Recipe.objects.create(
            title=template['title'],
            description=template['desc'],
            prep_time_minutes=template['time']
        )
        
        # 3. Create the Ingredients
        for ing_str in template['ingredients']:
            parts = ing_str.split('-', 1)
            Ingredient.objects.create(
                recipe=new_recipe,
                quantity=parts[0].strip(),
                name=parts[1].strip()
            )
            
    return redirect('home')