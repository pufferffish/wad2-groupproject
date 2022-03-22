from django.test import TestCase
from django.test import TestCase

import os
import re

from datetime import datetime, timedelta
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.forms import fields as django_fields

from OnlyPics.forms import UserInfoForm

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"


class OnlyPicsConfigurationTests(TestCase):
    """
    Tests the configuration of the Django project -- can cookies be used, at least on the server-side?
    """

    def test_middleware_present(self):
        """
        Tests to see if the SessionMiddleware is present in the project configuration.
        """
        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)

    def test_session_app_present(self):
        """
        Tests to see if the sessions app is present.
        """
        self.assertTrue('django.contrib.sessions' in settings.INSTALLED_APPS)

    def test_auth_app_present(self):
        """
        Tests to see if the sessions app is present.
        """
        self.assertTrue('microsoft_auth' in settings.INSTALLED_APPS)

    def test_installed_apps(self):
        """
        Checks whether the 'django.contrib.auth' app has been included in INSTALLED_APPS.
        """
        self.assertTrue('django.contrib.auth' in settings.INSTALLED_APPS)


class OnlyPicsFormClassTests(TestCase):
    """
      Do the Form classes exist, and do they contain the correct instance variables?
      """

    def test_form_exists(self):
        """
        Tests that the forms.py module exists in the expected location.
        """
        project_path = os.getcwd()
        rango_app_path = os.path.join(project_path, 'onlypics')
        forms_module_path = os.path.join(rango_app_path, 'forms.py')

        self.assertTrue(os.path.exists(forms_module_path),
                        f"{FAILURE_HEADER}We couldn't find Rango's new forms.py module. This is required to be created at the top of Section 7.2. This module should be storing your two form classes.{FAILURE_FOOTER}")

    def test_module_exists(self):
        """
        Tests that the forms.py module exists in the expected location.
        """
        project_path = os.getcwd()
        rango_app_path = os.path.join(project_path, 'onlypics')
        forms_module_path = os.path.join(rango_app_path, 'models.py')

        self.assertTrue(os.path.exists(forms_module_path),
                        f"{FAILURE_HEADER}We couldn't find Rango's new forms.py module. This is required to be created at the top of Section 7.2. This module should be storing your two form classes.{FAILURE_FOOTER}")

    """
    Checks whether the PageForm class has been implemented correctly.
    """

    def test_some_model_class(self):
        """
        Does the Model implementation exist, and does it contain the correct instance variables?
        """
        import OnlyPics.models
        import OnlyPics.forms

        self.assertTrue('UserInfoForm' in dir(OnlyPics.forms),
                        f"{FAILURE_HEADER}The class PageForm could not be found in OnlyPics's forms.py module.{FAILURE_FOOTER}")

        self.assertTrue('UserInfo' in dir(OnlyPics.models),
                        f"{FAILURE_HEADER}The class PageForm could not be found in OnlyPics's models.py module.{FAILURE_FOOTER}")

        self.assertTrue('Category' in dir(OnlyPics.models),
                        f"{FAILURE_HEADER}The class PageForm could not be found in OnlyPics's models.py module.{FAILURE_FOOTER}")

        self.assertTrue('Picture' in dir(OnlyPics.models),
                        f"{FAILURE_HEADER}The class PageForm could not be found in OnlyPics's models.py module.{FAILURE_FOOTER}")

        self.assertTrue('PictureVotes' in dir(OnlyPics.models),
                        f"{FAILURE_HEADER}The class PageForm could not be found in OnlyPics's models.py module.{FAILURE_FOOTER}")

        self.assertTrue('Comment' in dir(OnlyPics.models),
                        f"{FAILURE_HEADER}The class PageForm could not be found in OnlyPics's models.py module.{FAILURE_FOOTER}")

        userinfo = UserInfoForm()
        fields = userinfo.fields
        expected_fields = {
            'nickname': django_fields.CharField,
            'tokens': django_fields.IntegerField,
            'pfp': django_fields.FileField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(),
                            f"{FAILURE_HEADER}The field '{expected_field_name}' was not found in your UserInfoForm implementation.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]),
                             f"{FAILURE_HEADER}The field '{expected_field_name}' in UserInfoForm was not of the expected type '{type(fields[expected_field_name])}'.{FAILURE_FOOTER}")


class OnlyPicsTemplateTests(TestCase):
    """
     I think you should use template to implement some view.
     """

    def get_template(self, path_to_template):
        """
        Helper function to return the string representation of a template file.
        such as about.html index.html explore.html and so on
        """
        f = open(path_to_template, 'r')
        template_str = ""

        for line in f:
            template_str = f"{template_str}{line}"

        f.close()
        return template_str

    def test_base_template_exists(self):
        """
        Tests whether the base template exists.
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'onlypics', 'base.html')
        self.assertTrue(os.path.exists(template_base_path),
                        f"{FAILURE_HEADER}We couldn't find the new base.html template that's required in the templates/rango directory. Did you create the template in the right place?{FAILURE_FOOTER}")

    def test_base_title_block(self):
        """
        Checks if Rango's new base template has the correct value for the base template.
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'onlypics', 'base.html')
        template_str = self.get_template(template_base_path)

        title_pattern = r'<title>(\s*|\n*)OnlyPics(\s*|\n*)-(\s*|\n*){% block title_block %}(\s*|\n*)Base(\s*|\n*){% (endblock|endblock title_block) %}(\s*|\n*)</title>'
        self.assertTrue(re.search(title_pattern, template_str),
                        f"{FAILURE_HEADER}When searching the contents of base.html, we couldn't find the expected title block. ")

    def test_title_blocks(self):
        """
        perhaps you change the html file, then this test will fail, so change html file and test code at the same time
        :return:
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'onlypics')
        mappings = {
            reverse('onlypics:about'): {
                'full_title_pattern': r'<title>(\s*|\n*)OnlyPics(\s*|\n*)-(\s*|\n*)About OnlyPics(\s*|\n*)</title>',
                'block_title_pattern': r'{% block title_block %}(\s*|\n*)About OnlyPics(\s*|\n*){% (endblock|endblock title_block) %}',
                'template_filename': 'about.html'},

            reverse('onlypics:index'): {
                'full_title_pattern': r'<title>(\s*|\n*)OnlyPics(\s*|\n*)-(\s*|\n*)Homepage(\s*|\n*)</title>',
                'block_title_pattern': r'{% block title_block %}(\s*|\n*)Homepage(\s*|\n*){% (endblock|endblock title_block) %}',
                'template_filename': 'index.html'},

            reverse('onlypics:explore'): {
                'full_title_pattern': r'<title>(\s*|\n*)OnlyPics(\s*|\n*)-(\s*|\n*)Explore(\s*|\n*)</title>',
                'block_title_pattern': r'{% block title_block %}(\s*|\n*)Explore(\s*|\n*){% (endblock|endblock title_block) %}',
                'template_filename': 'explore.html'},
        }

        for url in mappings.keys():
            full_title_pattern = mappings[url]['full_title_pattern']
            template_filename = mappings[url]['template_filename']
            block_title_pattern = mappings[url]['block_title_pattern']
            request = self.client.get(url)
            content = request.content.decode('utf-8')
            template_str = self.get_template(os.path.join(template_base_path, template_filename))

            self.assertTrue(re.search(full_title_pattern, content),
                            f"{FAILURE_HEADER}When looking at the response of GET '{url}', we couldn't find the correct <title> block. Check the expected title.{FAILURE_FOOTER}")

            self.assertTrue(re.search(block_title_pattern, template_str),
                            f"{FAILURE_HEADER}When looking at the source of template '{template_filename}', we couldn't find the correct template block. Are you using template inheritence correctly{FAILURE_FOOTER}")

    def test_template_usage(self):
        """
        Check that each view uses the correct template.
        """
        urls = [reverse('onlypics:about'),
                reverse('onlypics:explore'),
                reverse('onlypics:index'), ]

        templates = ['onlypics/about.html',
                     'onlypics/explore.html',
                     'onlypics/index.html', ]

        for url, template in zip(urls, templates):
            response = self.client.get(url)
            self.assertTemplateUsed(response, template)

    def test_for_links_in_base(self):
        """
        There should be three hyperlinks in base.html, as per the specification of the book.
        Check for their presence, along with correct use of URL lookups.
        """
        template_str = self.get_template(os.path.join(settings.TEMPLATE_DIR, 'onlypics', 'base.html'))
        look_for = [
            '<a href="{% url \'onlypics:index\' %}">Home</a>',
            '<a href="{% url \'onlypics:explore\' %}">Explore</a>',
            '<a href="{% url \'onlypics:about\' %}">About</a>',
            '<a href="/microsoft/to-auth-redirect/?next=/onlypics/upload">Log in</a>',
        ]

        for lookup in look_for:
            self.assertTrue(lookup in template_str,
                            f"{FAILURE_HEADER}In base.html, we couldn't find the hyperlink '{lookup}'. Check your markup in base.html is correct and as written in the book.{FAILURE_FOOTER}")


class OnlyPicsViewTests(TestCase):
    """
    Tests the views manipulated.
    Specifically, changes to the index and about views.
    """
    """
    Performs checks to see if all the additional requirements in Chapter 7 for adding a CategoryForm have been implemented correctly.
    Checks URL mappings and server output.
    """

    def test_index_view(self):
        """
        """
        response = self.client.get(reverse('onlypics:index'))
        content = response.content.decode()
        self.assertTrue('<a href="/microsoft/to-auth-redirect/?next=/onlypics/upload">Log in</a>' in content)

        # self.assertTrue('visits:' not in content.lower(),
        #                 f"{FAILURE_HEADER}The index.html template should not contain any logic for displaying the number of views. Did you complete the exercises?{FAILURE_FOOTER}")

    def test_about_view(self):
        """
        Checks to see if the about view has the correct presentation for showing the number of visits.
        """
        response = self.client.get(reverse('onlypics:about'))
        content = response.content.decode()
        self.assertTrue('<a href="/microsoft/to-auth-redirect/?next=/onlypics/upload">Log in</a>' in content)

