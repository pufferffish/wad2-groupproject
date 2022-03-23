import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2Project10A.settings')
from datetime import datetime
import django
django.setup()
from OnlyPics.models import Picture, Category, UserInfo, User
from django.core.files.uploadedfile import UploadedFile

import random

images = {'Nature':['photoshoot2', 'photoshoot3', 'photoshoot4', 'photoshoot5', 'photoshoot6', 'photoshoot7',
                    'photoshoot8', 'photoshoot9', 'photoshoot10', 'photoshoot11', 'photoshoot12', 'photoshoot13'],
          'Animals':['cat', 'dog'],
          'Cities':['london', 'paris'],
          'Objects':['vase', 'photoshoot1']}

def read_images(images):
    user = UserInfo.objects.all()[0]

    for cat in images:
        category, ignored = Category.objects.get_or_create(name=cat)
        for img in images[cat]:
            file_path = os.path.join("populate_images", img + ".jpg")
            instance = Picture(
                owner=user,
                price=random.randint(0,100),
                name=img,
                tags=category,
                createdAt=datetime.now(),
                upload=UploadedFile(file=open(file_path, 'rb'))
            )
            instance.save()

if __name__ == '__main__':
    print("population images")
    read_images(images)
