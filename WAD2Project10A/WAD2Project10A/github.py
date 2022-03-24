import git
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path

@csrf_exempt
def update(request):
    repo = git.Repo("/home/octeep/wad2-groupproject")
    origin = repo.remotes.origin
    origin.pull()
    Path('/var/www/octeep_pythonanywhere_com_wsgi.py').touch()
    return HttpResponse("Updated code on PythonAnywhere")
