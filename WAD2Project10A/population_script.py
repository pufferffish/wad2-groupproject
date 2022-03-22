import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'WAD2Project10A.settings')
from datetime import datetime
import django
django.setup()
from OnlyPics.models import Picture, Category, UserInfo, User
from django.core.files.uploadedfile import UploadedFile

import random

images = {'Nature':['Photoshoot 2', 'Photoshoot 3', 'Photoshoot 4', 'Photoshoot 5', 'Photoshoot 6', 'Photoshoot 7',
                    'Photoshoot 8', 'Photoshoot 9', 'Photoshoot 10', 'Photoshoot 11', 'Photoshoot 12', 'Photoshoot 13'],
          'Animals':['cat', 'dog'],
          'Cities':['london', 'Paris'],
          'Objects':['vase', 'Photoshoot 1']}

def read_images(images):
    user = UserInfo.objects.all()[0]

    for cat in images:
        category = Category.objects.get(name=cat)
        for img in images[cat]:
            instance = Picture(
                owner=user,
                price=random.randint(0,100),
                name=img,
                tags=category,
                createdAt=datetime.now(),
                upload=UploadedFile(
                    file=open('populate_images\\' + img + '.JPG', 'rb')
                )
            )
            instance.save()

if __name__ == '__main__':
    print("population images")
    read_images(images)