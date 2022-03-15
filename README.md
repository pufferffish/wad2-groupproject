# READ THIS

The Microsoft OAuth mechanism requires setting some variable in the sites framework.
Run the content of [this script](WAD2Project10A/django_setup.py) in `python3 manage.py shell`
before testing anything.

Install all the required dependencies with `pip3.9 install -r requirements.txt`

To test the login mechanism, goto [/microsoft/to-auth-redirect/](http://localhost:8000/microsoft/to-auth-redirect/),
it should redirect you to Microsoft login site. use [/onlypics/whoami](http://localhost:8000/onlypics/whoami) to test if it works.


Project Idea:
    --> A site where which we can upload and sell images;
    --> ...

-------------------------------------------------------------------------------

Models:
    --> ...

-------------------------------------------------------------------------------

Util:
    --> Bootstrap;
    --> Django, V=2.2.26;
    --> JSON;
    --> Ajax;
    --> CSS;
    --> JavaScript;
    --> Python, V=3.9.x;
    --> Pillow, V=9.0.0;
    --> ...

-------------------------------------------------------------------------------

Initial Structure:
    --> Have one person do frontend dev;
    --> Have the rest break up according to the sample structure provided in-
        the group project web app file;
        --> The subsections will be:
            --> URLS;
            --> Models;
            --> Templates;
            --> User authentication;
            --> Unit testing;
            --> Views;
            --> JS, Bootstrap, Ajax.
    --> ...

-------------------------------------------------------------------------------

Main Ideas:
    --> 
