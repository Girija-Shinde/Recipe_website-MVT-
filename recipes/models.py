from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='category/',default='category/default.jpg')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=100)
    recipe_image = models.ImageField(upload_to='recipe/')
    recipe_description = models.TextField(help_text="Brief description of the recipe")
    ingredients = models.TextField(help_text="List of ingredients required")
    steps = models.TextField(help_text="Step-by-step instructions for preparation")
    categories = models.ManyToManyField(Category, blank=True, related_name='recipe')
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering= ['recipe_name']
        

    def __str__(self) :
        return self.recipe_name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together =('user', 'recipe')
    
    def __str__(self) :
        return f"Favorite by {self.user.username} for {self.recipe.recipe_name}"
                          