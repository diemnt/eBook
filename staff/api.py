from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from staff.models import Staff, Role
from staff.serializers import StaffSerializer, RoleSerializer, DisplayStaffSerializer
from django.conf import settings
from io import open
import traceback
import json
import os


@permission_classes((AllowAny,))
@api_view(['GET'])
def get_role_permissions(request, id):
    try:
        results = {}
        # Build path of permission file. Project path join file path
        permission_file_path = os.path.join(
            settings.BASE_DIR, 'websites/staff/permissions_default.json')

        # Open file with readonly.
        with open(permission_file_path, 'r') as permission_file:
            results['permissions_default'] = json.load(permission_file)

        # Get Role by Id
        role = Role.objects.get(pk=id)
        results["role"] = RoleSerializer(role).data
        return Response(results, status=200)

    except Role.DoesNotExist, e:
        return Response({"code": 400, "message": _("Role not found."), "fields": "id"}, status=400)

    except Exception, e:
        print 'GET Role Permission API Error: ', traceback.format_exc()
        return Response({"code": 500, "message": _("Internal Server Error"), "fields": ""}, status=500)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (AllowAny, )


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = StaffSerializer
    action_serializers = {
        'retrieve': DisplayStaffSerializer,
        'list': DisplayStaffSerializer,

    }

    # def partial_update(self, request, *args, **kwargs):
    #     serializer = StaffSerializer(data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)

    # Override get_serializer_class view : field role explain detail
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]

        return super(StaffViewSet, self).get_serializer_class()
