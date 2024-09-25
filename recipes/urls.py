from django.urls import path
from .views import *

urlpatterns = [
    path('', all_recipes, name='all_recipes'),
    path('categories/', list_categories, name='list_categories'),
    path('categories/<int:category_id>/', category_recipes, name='category_recipes'),
    path('add_recipe', add_recipe, name= 'add_recipe'),
    path('recipe/<int:id>/', recipe_detail, name='recipe_detail'),
    path('my_recipes/', my_recipes, name='my_recipes'),
    path('delete_recipe/<int:id>/', delete_recipe, name='delete_recipe'),
    path('update_/<int:id>/', update_recipe, name='update_recipe'),
    path('favorites/', my_favorites, name='my_favorites'),
    path('add_favorite/<int:recipe_id>', add_favorite, name='add_favorite'),
    path('remove_favorite/<int:recipe_id>', remove_favorite, name= 'remove_favorite'),


]
