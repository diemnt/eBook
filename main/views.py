# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.views import exception_handler

# Create your views here.


def custom_exception_handler(exc, context):
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        try:
            message = exc.detail.values()[0][0] if exc.detail else ""
            field = exc.detail.keys()[0] if exc.detail else ""
        except Exception, e:
            print "custom_exception_handler ", e
            message = "errors"
            field = ""

        response.data['code'] = response.status_code
        response.data['message'] = response.data[
            'detail'] if 'detail' in response.data else message
        response.data['fields'] = field
        if 'detail' in response.data:
            del response.data['detail']

    return response


def home(request):
    return render(request, 'websites/index.html')
