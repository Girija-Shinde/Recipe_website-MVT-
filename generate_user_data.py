import os
import django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_website.settings')
django.setup()

from custom_auth.models import UserProfile
from django.contrib.auth.models import User

fake = Faker()

# Create fake users and user profiles
def create_user_profiles(num=10):
    for _ in range(num):
        user = User.objects.create_user(
            username=fake.user_name(),
            # password=fake.password(),
            password = 'User@123',
            email=fake.email()
        )
        UserProfile.objects.create(
            user=user,
            bio=fake.paragraph(nb_sentences=2),
            profile_pic='profile_pics/default_profile.jpg'  # Default image
        )

if __name__ == '__main__':
    create_user_profiles()
