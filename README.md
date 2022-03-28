# READ THIS

The Microsoft OAuth mechanism requires setting some variable in the sites framework.
Run the content of [this script](WAD2Project10A/django_setup.py) in `python3 manage.py shell`
before testing anything.

To populate the database with sample data, run [the population script](WAD2Project10A/population_script.py).

To run the unit tests, run `python3 manage.py test`.

Install all the required dependencies with `pip3 install -r requirements.txt`.

To test locally, here is a list of command to get started:
```
git clone https://github.com/octeep/wad2-groupproject.git
cd wad2-groupproject/WAD2Project10A
python3 manage.py makemigrations
python3 manage.py makemigrations OnlyPics
python3 manage.py migrate
python3 manage.py shell < django_setup.py
python3 manage.py runserver
```

The site is hosted at [octeep.pythonanywhere.com](https://octeep.pythonanywhere.com).
