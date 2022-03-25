import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2Project10A.settings')
from datetime import datetime
import django

django.setup()
from OnlyPics.models import Picture, Category, UserInfo, User
from django.core.files.uploadedfile import UploadedFile

import random
from faker import Faker

# ensure population data are consistent
random.seed(0xDEADBEEF)
Faker.seed(0xDEADBEEF)
faker = Faker()

images = {
    'Nature':  [f'photoshoot{i}' for i in range(2, 14)],
    'Animals': ['cat', 'dog'],
    'Cities':  ['london', 'paris'],
    'Objects': ['vase', 'photoshoot1']
}

usernames = [faker.name() for i in range(12)]

def populate_users():
    i = 0
    for username in usernames:
        i += 1
        django_user, ignored = User.objects.get_or_create(username = f"testuser{i}")
        django_user.save()
        user, ignored = UserInfo.objects.get_or_create(user=django_user)
        user.nickname = username
        user.save()

def populate_images(images):
    for cat in images:
        category, ignored = Category.objects.get_or_create(name=cat)
        for img in images[cat]:
            user = UserInfo.objects.get(nickname = random.choice(usernames))
            file_path = os.path.join("populate_images", img + ".jpg")
            instance = Picture(
                owner=user,
                price=random.randint(0, 100),
                name=img,
                tags=category,
                createdAt=faker.date_time_this_year(),
                upload=UploadedFile(file=open(file_path, 'rb'))
            )
            instance.save()


if __name__ == '__main__':
    print("populating fake users")
    populate_users()
    print("populating images and categories")
    populate_images(images)
