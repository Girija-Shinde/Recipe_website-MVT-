from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'recipe_image', 'recipe_description', 'ingredients','steps','categories']
        widgets = {
            'recipe_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipe Name'}),
            'recipe_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'recipe_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Brief description of the recipe'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List of ingredients'}),
            'steps': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Step-by-step instructions'}),
            'categories': forms.CheckboxSelectMultiple(),
        }

    def clean_recipe_name(self):
        recipe_name = self.cleaned_data.get('recipe_name')
        # Check if the recipe name is unique, except for the current instance being updated
        if Recipe.objects.filter(recipe_name=recipe_name).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('A recipe with this name already exists.')
        return recipe_name