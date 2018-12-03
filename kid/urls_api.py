from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from kid import api
# from django.contrib import admin

urlpatterns = [
    url(r'^kid/login/$', api.authenticate_kid, name="kid-login"),
    url(r'^kid/check/authenticate/$', api.check_authenticate, name="kid-check-authenticate"),
    url(r'^accounts/login/$', obtain_jwt_token, name="accounts-login"),
]
