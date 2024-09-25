from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Category, Recipe, Favorite
from .forms import RecipeForm
import random
# Create your views here

def chunk_list(lst, chunk_size):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def home(request):
    # Get the most recent 6 recipes for the grid view
    recent_recipes = Recipe.objects.order_by('-created_at')[:6]
    
    # Get all categories and chunk them for carousel display
    categories = Category.objects.all()
    chunked_categories = list(chunk_list(categories, 3))
    
    # Get all recipes and select 6 random recipes for the carousel
    all_recipes = list(Recipe.objects.all())
    random_recipes = random.sample(all_recipes, min(len(all_recipes), 6))
    
    return render(request, 'index.html', {
        'title': 'Home',
        'recent_recipes': recent_recipes,
        'chunked_categories': chunked_categories,
        'random_recipes': random_recipes,
    })

def list_categories(request):
    search_query = request.GET.get('search')
    if search_query:
        categories = Category.objects.filter(name__icontains=search_query)
    else:
        categories= Category.objects.all()

    return render(request, 'recipes/categories.html', {'categories': categories, 'title':'Category', 'search_query': search_query})

def all_recipes(request):
    search_query = request.GET.get('search', '')
    if search_query:
        recipes = Recipe.objects.filter(recipe_name__icontains = search_query) | Recipe.objects.filter(ingredients__icontains = search_query) | Recipe.objects.filter(categories__name__icontains= search_query)
    else:
        recipes = Recipe.objects.all()
    
    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    favorite_recipes = []
    if request.user.is_authenticated:
        favorite_recipes = Favorite.objects.filter(user =request.user).values_list('recipe_id', flat = True)

    return render(request, 'recipes/all_recipes.html',{'page_obj': page_obj, 'title': 'Recipes', 'search_query': search_query, 'favorite_recipes': favorite_recipes,})

def category_recipes(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    search_query = request.GET.get('search', '')
    get_category =Recipe.objects.filter(categories = category)

    if search_query:
        recipes = get_category.filter(recipe_name__icontains = search_query)| get_category.filter(ingredients__icontains= search_query)
    else:
        recipes = get_category

    paginator = Paginator(recipes, 9)
    page_number  = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    favorite_recipes = []
    if request.user.is_authenticated:
        favorite_recipes = Favorite.objects.filter(user =request.user).values_list('recipe_id', flat = True)

    return render(request, 'recipes/category_recipes.html',{'page_obj': page_obj, 'category': category, 'title': category, 'search_query': search_query, 'favorite_recipes': favorite_recipes})

@login_required(login_url='login')
def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    favorite_recipes = Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True) if request.user.is_authenticated else []
    
    context = {
        'recipe': recipe,
        'title': recipe.recipe_name,
        'favorite_recipes': favorite_recipes
    }
    return render(request, 'recipes/recipe_detail.html', context)

@login_required(login_url='login')
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe= form.save(commit = False)
            recipe.user = request.user
            recipe.save()
            form.save_m2m()  # This is important for saving many-to-many relationships like categories
            messages.success(request, 'Recipe added successfully!')
            return redirect('all_recipes')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html',{'form': form, 'title': 'Add Recipe', 'button_text': 'Add Recipe'})

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(user = request.user)

    paginator = Paginator(recipes, 9)  # Show 9 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'recipes/my_recipes.html',{'page_obj':page_obj, 'title': 'My Recipes'})

@login_required
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, user= request.user)
    recipe.delete()
    messages.success(request, "Recipe deleted successfully")
    return redirect('my_recipes')

@login_required
def update_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe updated successfully!")
            return redirect('my_recipes')
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipes/add_recipe.html', {'form': form, 'title': 'Update Recipe', 'button_text': 'Update Recipe'})

@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    recipes = [favorite.recipe for favorite in favorites]

    paginator = Paginator(recipes, 9)  # Show 9 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/my_favorites.html', {'page_obj': page_obj, 'title': 'My Favorites'})

@login_required(login_url='login')
def add_favorite(request,recipe_id):
    recipe= get_object_or_404(Recipe, id= recipe_id)
    Favorite.objects.get_or_create(user =request.user, recipe = recipe)
    next_url = request.GET.get('next', 'all_recipes')
    return redirect(next_url)

@login_required
def remove_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id = recipe_id)
    favorite = Favorite.objects.filter(user = request.user, recipe = recipe)
    if favorite:
        favorite.delete()
    next_url = request.GET.get('next', 'all_recipes')
    return redirect(next_url)