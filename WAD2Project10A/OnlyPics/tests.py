from django.db.models import OneToOneField, CharField, PositiveIntegerField, ForeignKey, IntegerField, CASCADE, \
    TextField
from django.test import TestCase

import os
import re
import uuid

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
    user, ignored = User.objects.get_or_create(username='testuser' + str(uuid.uuid4()))
    user.set_password('testabc123')
    user.save()
    user_info, ignored = UserInfo.objects.get_or_create(user=user)
    user_info.nickname = str(uuid.uuid4())
    user_info.save()

    return user


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
        self.client.login(username=user.username, password='testabc123')
        response = self.client.get(reverse('onlypics:edit_account'))
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to edit profile when logged in. Check your test_user_can_edit_account() view.{FAILURE_FOOTER}")

    def test_user_can_delete_account(self):
        """
        user can change profile name
        user can change profile icon
        """
        user = create_user_object()
        self.client.login(username=user.username, password='testabc123')
        response = self.client.get(reverse('onlypics:delete_account'))
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to delete user when logged in. Check your test_user_can_delete_account() view.{FAILURE_FOOTER}")

    def test_user_can_buy(self):
        """
        user can buy
        """
        user = create_user_object()
        self.client.login(username=user.username, password='testabc123')
        response = self.client.get(reverse('onlypics:explore'))
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to buy pictures when logged in. Check test_user_can_buy() view.{FAILURE_FOOTER}")

    def test_user_can_sell(self):
        user = create_user_object()
        self.client.login(username=user.username, password='testabc123')
        response = self.client.get(reverse('onlypics:post_for_sale'))
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to sell pictures when logged in. Check your test_user_can_sell() view.{FAILURE_FOOTER}")
