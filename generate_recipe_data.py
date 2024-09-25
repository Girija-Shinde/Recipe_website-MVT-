import os
import django
import random
from faker import Faker

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_website.settings')

django.setup()

from custom_auth.models import UserProfile
from recipes.models import Category, Recipe  # Replace 'your_app' with the actual app name

fake = Faker()

def create_recipes(num=10):
    users = UserProfile.objects.all()
    categories = Category.objects.all()

    if not categories.exists():
        print("No categories found. Please create some categories first.")
        return

    for _ in range(num):
        recipe = Recipe.objects.create(
            user=random.choice(users).user,  # Randomly assign a user
            recipe_name=fake.sentence(nb_words=3),
            recipe_image='recipe/vada_pav.jpg',  # Ensure you have a default image
            recipe_description=fake.paragraph(nb_sentences=3),
            ingredients=fake.paragraph(nb_sentences=2),
            steps=fake.paragraph(nb_sentences=4)
        )
        # Assign 1 to 3 random categories to the recipe
        assigned_categories = random.sample(list(categories), k=random.randint(1, 3))
        recipe.categories.set(assigned_categories)

if __name__ == '__main__':
    create_recipes()
