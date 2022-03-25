from django.db.models import OneToOneField, CharField, PositiveIntegerField, ForeignKey, IntegerField, CASCADE, \
    TextField
from django.test import TestCase

import os
import re

from datetime import datetime, timedelta
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.forms import fields as django_fields
from django.contrib.auth.models import User
from django_resized import ResizedImageField

import OnlyPics
from OnlyPics.forms import UserInfoForm
from OnlyPics.models import Category, Picture, UserInfo, Comment

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


def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user


class OnlyPicsFormModuleClassTests(TestCase):
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

    def test_some_form_class(self):
        """
        Does the Model implementation exist, and does it contain the correct instance variables?
        """
        import OnlyPics.forms
        self.assertTrue('UserInfoForm' in dir(OnlyPics.forms),
                        f"{FAILURE_HEADER}The class PageForm could not be found in OnlyPics's forms.py module.{FAILURE_FOOTER}")

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

    def test_some_model_exist(self):
        import OnlyPics.models
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

    def test_model_UserInfo(self):
        user_profile = OnlyPics.models.UserInfo()
        # Now check that all the required attributes are present.
        # We do this by building up a UserProfile instance, and saving it.

        expected_attributes = {
            'user': create_user_object(),
            'nickname': 'testnickname',
            'tokens': 100,
            'pfp': None
        }

        expected_types = {
            'user': OneToOneField,
            'nickname': CharField,
            'tokens': PositiveIntegerField,
            'pfp': ResizedImageField
        }

        found_count = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1
                    self.assertEqual(type(attr), expected_types[attr_name],
                                     f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserInfo model.{FAILURE_FOOTER}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])
        self.assertEqual(found_count, len(expected_attributes.keys()),
                         f"{FAILURE_HEADER}In the UserInfo model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Check your implementation and try again.{FAILURE_FOOTER}")
        user_profile.save()

    def test_model_Category(self):
        category = Category()
        # Now check that all the required attributes are present.
        # We do this by building up a UserProfile instance, and saving it.

        expected_attributes = {
            'name': 'testnickname',
        }

        expected_types = {
            'name': CharField,
        }

        found_count = 0

        for attr in category._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1
                    self.assertEqual(type(attr), expected_types[attr_name],
                                     f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserInfo model.{FAILURE_FOOTER}")
                    setattr(category, attr_name, expected_attributes[attr_name])
        self.assertEqual(found_count, len(expected_attributes.keys()),
                         f"{FAILURE_HEADER}In the UserInfo model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Check your implementation and try again.{FAILURE_FOOTER}")
        category.save()


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

    def test_about_view(self):
        """
        Checks to see if the about view has the correct presentation for showing the number of visits.
        """
        response = self.client.get(reverse('onlypics:about'))
        content = response.content.decode()
        self.assertTrue('<a href="/microsoft/to-auth-redirect/?next=/onlypics/upload">Log in</a>' in content)

    def test_explore_view(self):
        response = self.client.get(reverse('onlypics:explore'))
        content = response.content.decode()
        self.assertTrue('<a href="/microsoft/to-auth-redirect/?next=/onlypics/upload">Log in</a>' in content)

    def test_vbucks(self):
        response = self.client.get(reverse('onlypics:vbucks'))
        content = response.content.decode()
        self.assertTrue('csrfmiddlewaretoken' in content)


class OnlyPicsFunctionTests(TestCase):
    """
    A series of tests to check function implemented correctly.
    """

    def test_user_can_edit_account(self):
        """
        user can change profile name
        user can change profile icon
        """
        user = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get(reverse('onlypics:edit_account'))
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to edit profile when logged in. Check your edit_profile() view.{FAILURE_FOOTER}")

        content = response.content.decode()
        self.assertTrue('' in content,
                        f"{FAILURE_HEADER}When edit profile (when logged in), we didn't see the expected page. Please check your edit profile() view.{FAILURE_FOOTER}")

    def test_user_can_delete_account(self):
        """
        user can change profile name
        user can change profile icon
        """
        user = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get(reverse('onlypics:delete_account'))
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to edit profile when logged in. Check your edit_profile() view.{FAILURE_FOOTER}")

        content = response.content.decode()
        self.assertTrue('' in content,
                        f"{FAILURE_HEADER}When edit profile (when logged in), we didn't see the expected page. Please check your edit profile() view.{FAILURE_FOOTER}")

    def test_user_can_post(self):
        """
        user can upload
        """
        user = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get(reverse('onlypics:upload'))
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to edit profile when logged in. Check your edit_profile() view.{FAILURE_FOOTER}")

        content = response.content.decode()
        self.assertTrue('' in content,
                        f"{FAILURE_HEADER}When edit profile (when logged in), we didn't see the expected page. Please check your edit profile() view.{FAILURE_FOOTER}")

    def test_user_can_comment(self):
        """
        user can comment
        """
        user = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get(reverse('onlypics:upload'))

        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to edit profile when logged in. Check your edit_profile() view.{FAILURE_FOOTER}")

        content = response.content.decode()
        self.assertTrue('' in content,
                        f"{FAILURE_HEADER}When edit profile (when logged in), we didn't see the expected page. Please check your edit profile() view.{FAILURE_FOOTER}")

    def test_user_can_buy(self):
        """
        user can buy
        """
        user = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get(reverse('onlypics:explore'))
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to edit profile when logged in. Check your edit_profile() view.{FAILURE_FOOTER}")

        content = response.content.decode()
        self.assertTrue('' in content,
                        f"{FAILURE_HEADER}When edit profile (when logged in), we didn't see the expected page. Please check your edit profile() view.{FAILURE_FOOTER}")

    def test_user_can_sell(self):
        user = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get(reverse('onlypics:post_for_sale'))
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to edit profile when logged in. Check your edit_profile() view.{FAILURE_FOOTER}")

        content = response.content.decode()
        self.assertTrue('' in content,
                        f"{FAILURE_HEADER}When edit profile (when logged in), we didn't see the expected page. Please check your edit profile() view.{FAILURE_FOOTER}")

    def test_user_can_look_private(self):
        pass
