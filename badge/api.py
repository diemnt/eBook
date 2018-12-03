# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from badge.models import *
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, mixins
from serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from staff.permission_class import RolePermission
from staff.decorators import check_role_permission
from rest_framework.parsers import MultiPartParser,JSONParser
from rest_framework import status



'''
    ******  START STAFF MODULE  ********
'''


class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = (RolePermission, )
    parser_classes = (MultiPartParser, JSONParser)
    
    # Add created_by current staff
    def perform_create(self, serializer):
        serializer.save( created_by = self.request.user.staff )

    # Add modified_by current staff
    def perform_update(self, serializer):
        serializer.save( modified_by = self.request.user.staff )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Delete Badge don't has kid and unactive
        badge_valid = Badge.objects.filter(id = instance.id, kidbadges_badges_rel__isnull=True, is_active = False)
        if badge_valid:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"code": 400, 'message': _('Không thể xóa huy chương.')}, status=400)


'''
    Funtion delete_list_badge
    Delete list bage
    Author: Hoang nguyen
'''


@api_view(['DELETE'])
@check_role_permission('badge_delete')
def delete_list_badge(request):
    try:
        list_badge = request.data.get('list_badge', None)
        # Delete badge which unactive and not kid has
        if list_badge:
            badge = Badge.objects.filter(
                id__in=list_badge, kidbadges_badges_rel__isnull=True, is_active = False)
            list_badge_valid = badge.values_list('id', flat = True)
            
            # If list_badge is in list_badge_valid then delete
            check_sub_set = set(list_badge).issubset(set(list_badge_valid))
            if check_sub_set:
                badge.delete()
                return Response({'message': _('Thành công.')})
            return Response({"code": 400, 'message': _('Không thể xóa huy chương.')}, status=400)
        return Response({"code": 400, "message": _("Danh sách huy chương là bắt buộc.")}, status=400)
    except Exception, e:
        print 'delete_list_badge ', e
        return Response({"code": 500, "message": _("Lỗi hệ thống."), "fields": ""}, status=500)

'''
    Funtion change_active_badge
    Change active bage
    Author: Hoang nguyen
'''


@api_view(['PUT'])
@check_role_permission('badge_attr_is_active')
def change_active_badge(request, id):
    try:
        badge = Badge.objects.get(id = id )
        status_active = request.data.get('is_active', None)
        if status_active is not None:
            badge.is_active = True if status_active else False
            badge.save()
            return Response({'message': _('Thành công.')})
        return Response({"code": 400, 'message': _('Không tìm thấy trạng thái huy chương.')}, status=400)

    except Badge.DoesNotExist, e:
        return Response({"code": 400, "message": _("Không tìm thấy huy chương này"), "fields": ""}, status=400)
    except Exception, e:
        print 'delete_list_badge ', e
        return Response({"code": 500, "message": _("Lỗi hệ thống."), "fields": ""}, status=500)



'''
    ******  END STAFF MODULE  ********
'''

