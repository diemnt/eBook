# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_fsm import TransitionNotAllowed
import json
from organization.models import Package
from organization.serializers import PackageSerializer

@api_view(['PATCH'])
@permission_classes((AllowAny,))
def change_package_state(request, package_id):
    try:
        status = request.data.get('status', None)
        if not status:
            return Response({"code": 400, "message": _(u"Trường trạng thái là bắt buộc. Vui lòng kiểm tra lại"), "fields": "status"}, status=400)    
        
        package = Package.objects.get(pk=package_id)
        
        # Get method by name status
        method_transition = getattr(package, status)
        # Execute method transition check valid status
        method_transition()
        package.save()
        result = PackageSerializer(package)
        return Response(data=result.data, status=200)

    except TransitionNotAllowed as e:
        print "## TransitionNotAllowed ",e.message
        return Response({"code": 400, "message": str(e.message), "fields": "status"}, status=400)
    except AttributeError:
        return Response({"code": 400, "message": _(u"Dữ liệu trạng thái không hợp lệ"), "fields": "status"}, status=400)
    except Package.DoesNotExist, e:
        return Response({"code": 400, "message": _(u"Không tìm thấy gói dịch vụ. Vui lòng kiểm tra lại"), "fields": ""}, status=400)
    except Exception, e:
        print "Error Organization change_package_state ",e
        return Response({"code": 500, "message": _(u"Lỗi hệ thống."), "fields": ""}, status=500)
