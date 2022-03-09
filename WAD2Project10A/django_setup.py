from django.contrib.sites.models import Site
one = Site.objects.all()[0]
one.domain = 'localhost:8000'
one.name = 'OnlyPics'
one.save()
