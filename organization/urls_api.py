from rest_framework import routers
from django.conf.urls import url, include
from organization import api_viewset


router = routers.DefaultRouter()
router.register(r'admin/operation//organization/package', api_viewset.PackageViewSet)
router.register(r'admin/operation/organization', api_viewset.OrganizationViewSet)

urlpatterns = [
    # url(r'^admin/operation/organization/package/(?P<id>[0-9]+)/state/$', api.change_active_badge, name='change-state-badge'),
    url(r'^', include(router.urls)),
]
