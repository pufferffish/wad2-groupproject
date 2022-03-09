from django import forms
from django.conf import settings
import requests

CAPTCHA_SECRET_KEY = settings.HCAPTCHA_SECRET_KEY
CAPTCHA_FORM_KEY = "h-captcha-response"
CAPTCHA_VERIFY_URL = "https://hcaptcha.com/siteverify"

# generic Exception for captcha errors
class CaptchaException(Exception):
    pass

# thrown when the request does not contain valid hcaptcha token
class CaptchaInvalidInputException(CaptchaException):
    pass

# thrown when hcaptcha says the token is invalid
class CaptchaInvalidTokenException(CaptchaException):
    def __init__(self, reason):
        self.reason = reason

# Give a hcaptcha token, returns unit, or throw an error if it fails to verify for whatever reason.
def verify_hcaptcha_token(token):
    if token == '':
        raise CaptchaInvalidInputException()
    data = { 'secret': CAPTCHA_SECRET_KEY, 'response': token }
    response = requests.post(url=CAPTCHA_VERIFY_URL, params=data, timeout=10).json()
    if not response['success']:
        raise CaptchaInvalidTokenException(response['error-codes'])

# Given a request, returns unit, throw an error if it fails to verify for whatever reason.
def verify_hcaptcha_request(request):
    if CAPTCHA_FORM_KEY not in request.POST:
        raise CaptchaInvalidTokenException()
    token = (request.POST)[CAPTCHA_FORM_KEY]
    verify_hcaptcha_token(token)

# HCaptcha says the token is only valid 'within a short period of time after being issued'.
# They didn't provide the exact duration, but they do provide the timestamp when the captcha
# was solved. We can probably implement our own checks to prevent a token that is too old.
# However, the timestamp they send is in ISO 8601 format, and Python base library doesn't
# support it unfortunately, meaning that we would need another library to do so.
# As such, I will just leave it be.
