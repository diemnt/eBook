from django.conf.urls import url, include
import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'admin/operation/badge/badge', api.BadgeViewSet)



urlpatterns = [
    url(r'^admin/operation/badge/badge/list/$', api.delete_list_badge, name='delete-list-badge'),
    url(r'^admin/operation/badge/badge/(?P<id>[0-9]+)/state/$', api.change_active_badge, name='change-state-badge'),
    url(r'^', include(router.urls)),


]
    