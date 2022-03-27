import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2Project10A.settings')
from datetime import datetime
import django

django.setup()
from OnlyPics.models import *
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
    users = []
    for username in usernames:
        i += 1
        django_user, ignored = User.objects.get_or_create(username = f"testuser{i}")
        django_user.save()
        user, ignored = UserInfo.objects.get_or_create(user=django_user)
        user.nickname = username
        user.save()
        users.append(user)
    return users

def populate_images(images):
    pictures = []
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
            pictures.append(instance)
    return pictures


def populate_comments(users, pictures):
    for i in range(18):
        picture = random.choice(pictures)
        user = random.choice(users)
        Comment(owner = user, picture = picture, text = faker.sentence(), made_at = faker.date_time_this_year()).save()

if __name__ == '__main__':
    print("populating fake users")
    users = populate_users()
    print("populating images and categories")
    pictures = populate_images(images)
    print("populating comments")
    populate_comments(users, pictures)
