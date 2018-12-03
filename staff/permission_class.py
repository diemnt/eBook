from staff.models import Staff, StaffRole
from rest_framework import permissions
from django.contrib.postgres.aggregates import StringAgg
from django.utils.translation import ugettext_lazy as _


class RolePermission(permissions.BasePermission):
    message = _("Forbidden")

    def get_action_name(self, method_name):
        switcher = {
            'post': 'add',
            'put': 'edit',
            'patch': "edit",
            'delete': "delete",
        }
        return switcher.get(method_name, method_name)

    def has_permission(self, request, view):
        try:
            # Check user is staff.
            if not request.user.is_staff:
                self.message = _("User not is staff.")
                print "User not is staff."
                return False

            print "staff", request.user.user_staff_rel
            # Get staff object from current user ( Staff and User rel OneToOne)
            staff = request.user.user_staff_rel

            # With method then not check role permission. All staff can get
            # data
            if request.method == "GET":
                return True

            # Get model from view
            model_name = view.basename
            action_name = self.get_action_name(request.method.lower())
            # Create permission key.
            permission_key = "{0}_{1}".format(model_name, action_name)
            return staff.has_role_permission(permission_key)

        except Staff.DoesNotExist, e:
            print "ERROR: Staff Not Found."
            return False
        except Exception, e:
            print "ERROR: Internal Server Error.", e
            return False
