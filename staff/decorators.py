# -*- coding: utf-8 -*-
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from staff.models import Staff, StaffRole
from django.contrib.postgres.aggregates import StringAgg

"""
    Decorator check permission. apply with admin operation
    If check single key then call @check_role_permission("ebook_add")
    If check muilple key then call @check_role_permission(["ebook_add", "category_add"])
"""


def check_role_permission(permission_key):
    def wrapper(view_func):
        def wrapped(request, *args, **kwargs):
            print "Check role permission"
            try:
                # Check user is authenticated.
                if not request.user.is_authenticated():
                    return Response({"code": 401, "message": _("Unauthorized"), "fields": ""}, status=401)

                # Check user is staff.
                if not request.user.is_staff:
                    return Response({"code": 403, "message": _("User not is staff."), "fields": ""}, status=403)

                # Get staff object from current user ( Staff and User rel
                # OneToOne)
                staff = request.user.user_staff_rel

                # Check permission key params valid
                if not permission_key:
                    print "Permission key empty."
                    return Response({"code": 403, "message": _("Forbidden"), "fields": ""}, status=403)

                # Check role permission
                if not staff.has_role_permission(permission_key):
                    return Response({"code": 403, "message": _("Forbidden"), "fields": ""}, status=403)

                return view_func(request, *args, **kwargs)

            except Staff.DoesNotExist, e:
                print "ERROR: Staff Not Found."
                return Response({"code": 403, "message": _("User not is staff."), "fields": ""}, status=403)
            except Exception, e:
                print "ERROR: Internal Server Error.", e
                return Response({"code": 500, "message": _("Internal Server Error"), "fields": ""}, status=500)

        return wrapped
    return wrapper
