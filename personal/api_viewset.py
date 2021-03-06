# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import mixins
from personal.serializers import PackageSerializer, PersonalSerializer
from personal.models import Package, Personal


class PackageViewSet(viewsets.ModelViewSet):

    queryset = Package.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = PackageSerializer

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status != 'draft':
            return Response(data={'message': u"Không thể xoá gói dịch vụ khi đang ở trạng thái %s" % obj.status},
                            status=status.HTTP_400_BAD_REQUEST)
        return super(PackageViewSet, self).destroy(request, *args, **kwargs)


class PersonalViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):

    queryset = Personal.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = PersonalSerializer
   