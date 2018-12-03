# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from core.models import *
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from staff.permission_class import RolePermission
from staff.decorators import check_role_permission
from django.db.models import Q
from rest_framework import status


CUSTOMER_LIST = '/customers/list-orgnizationa/'

'''
    ******  START STAFF MODULE  ********
'''


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    permission_classes = (RolePermission, )

    def get_serializer_class(self):
        if self.action == 'list':
            return DisplayLevelSerializer
        return LevelSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Delete level don't has published book
        level_has_book = instance.book_set.filter(status = 'published')
        if level_has_book:
            return Response({"code": 400, 'message': _('Không thể xóa cấp độ.')}, status=400)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
    Funtion delete_list_level
    Delete list level
    Author: Hoang nguyen
'''
@api_view(['DELETE'])
@check_role_permission('level_delete')
def delete_list_level(request):
    try:
        list_level = request.data.get('list_level', None)
        # Delete level which has no published book
        if list_level:
            level = Level.objects.filter( Q(id__in=list_level), ~Q(book__status = 'published'))
            list_level_valid = level.values_list('id', flat = True)
            
            # If list level is in list_level_valid then delete
            check_sub_set = set(list_level).issubset(set(list_level_valid))
            if check_sub_set:
                level.delete()
                return Response({'message': _('Thành công.')})
            return Response({"code": 400, 'message': _('Không thể xóa cấp độ.')}, status=400)
        return Response({"code": 400, "message": _("Danh sách cấp độ là bắt buộc.")}, status=400)
    except Exception, e:
        print 'delete_list_level ', e
        return Response({"code": 500, "message": _("Lỗi hệ thống"), "fields": ""}, status=500)




class CategoryBookViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    permission_classes = (RolePermission, )

    def get_serializer_class(self):
        if self.action == 'list':
            return DisplayBookCategorySerializer
        return BookCategorySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Delete Category don't has published book
        category_has_book = instance.book_set.filter(status = 'published')
        if category_has_book:
            return Response({"code": 400, 'message': _('Không thể xóa danh mục.')}, status=400)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
    Funtion delete_list_category
    Delete list category
    Author: Hoang nguyen
'''


@api_view(['DELETE'])
@check_role_permission('bookcategory_delete')
def delete_list_category(request):
    try:
        list_category = request.data.get('list_category', None)
        # Delete category which has no published book
        if list_category:
            category = BookCategory.objects.filter( Q(id__in=list_category), ~Q(book__status = 'published'))
            list_category_valid = category.values_list('id', flat = True)
            
            # If list category is in list_category_valid then delete
            check_sub_set = set(list_category).issubset(set(list_category_valid))
            if check_sub_set:
                category.delete()
                return Response({'message': _('Thành công.')})
            return Response({"code": 400, 'message': _('Không thể xóa danh mục.')}, status=400)
        return Response({"code": 400, "message": _("Danh sách danh mục là bắt buộc.")}, status=400)
    except Exception, e:
        print 'delete_list_category ', e
        return Response({"code": 500, "message": _("Lỗi hệ thống"), "fields": ""}, status=500)






'''
    ******  END STAFF MODULE  ********
'''
