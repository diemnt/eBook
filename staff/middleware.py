from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import threading
from django.core.exceptions import ObjectDoesNotExist

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # Django < 1.10
    # Works perfectly for everyone using MIDDLEWARE_CLASSES
    MiddlewareMixin = object

"""
    Middleware set current staff login.
"""


class CurrentStaffMiddleware(MiddlewareMixin):
    """
    Always have access to the current user
    """
    __staffs = {}

    def process_request(self, request):
        """
        Store user info
        """
        user = SimpleLazyObject(
            lambda: self.__class__.get_jwt_user(request))
        """
            1. Check only apply for staff operation API 
            2. Check user is authenticated
            3. Check user is staff
        """
        if '/admin/operation/' in request.path and user.is_authenticated() and user.is_staff:
            print "USER", user
            try:
                self.__class__.set_staff(user.user_staff_rel)
            except ObjectDoesNotExist:
                print "Middleware::: User invalid. User not have staff record"
                pass

    def process_response(self, request, response):
        """
        Delete user info
        """
        self.__class__.del_staff()
        return response

    def process_exception(self, request, exception):
        """
        Delete user info
        """
        self.__class__.del_staff()

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        jwt_authentication = JSONWebTokenAuthentication()
        if jwt_authentication.get_jwt_value(request):
            user, jwt = jwt_authentication.authenticate(request)

        return user

    @classmethod
    def get_staff(cls, default=None):
        """
        Retrieve user info
        """
        return cls.__staffs.get(threading.current_thread(), default)

    @classmethod
    def set_staff(cls, staff):
        """
        Store user info
        """
        cls.__staffs[threading.current_thread()] = staff

    @classmethod
    def del_staff(cls):
        """
        Delete user info
        """
        cls.__staffs.pop(threading.current_thread(), None)
