from django.contrib import admin
from .models import Category, Recipe, Favorite
# Register your models here.
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Favorite)