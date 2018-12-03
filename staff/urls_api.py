from rest_framework import routers
from django.conf.urls import url, include
from staff import api


router = routers.DefaultRouter()
router.register(r'admin/operation/staff', api.StaffViewSet)
router.register(r'admin/operation/role', api.RoleViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/operation/role/(?P<id>[0-9]+)/permissions/$',
        api.get_role_permissions, name='get-role-permissions'),
]
