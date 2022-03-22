import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'WAD2Project10A.settings')
from PIL import Image
import datetime
import django
django.setup()
from OnlyPics.models import Picture, Category, UserInfo
from django.core.files.images import ImageFile

def read_images():
    pop_text = "Photoshoot"
    im = Image.open("C:/Users/kalfo/Documents/University2/Semester 2/WAD2/pop/Photoshoot 1.JPG")
    im.show()

    user = UserInfo.objects.get(nickname="iliyan")
    cat = Category.objects.get(name="Nature")
    d = datetime.datetime.utcnow()

    i = Picture.objects.get_or_create(owner=user, price=50, name="flower", tags=cat)[0]
    img = ImageFile(open("C:/Users/kalfo/Documents/University2/Semester 2/WAD2/pop/Photoshoot 1.JPG", "rb"))
    i.upload = img
    i.save()

def add_picture(owner, price, name, category, createdAt, image):
    picture = Picture.objects.get_or_create(owner=owner)

if __name__ == '__main__':
    print("Showing images")
    read_images()
