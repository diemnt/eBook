from django.conf.urls import url, include
import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'admin/operation/core/level', api.LevelViewSet)
router.register(r'admin/operation/core/book/category', api.CategoryBookViewSet)




urlpatterns = [
    url(r'^admin/operation/core/level/list/$', api.delete_list_level, name='delete-list-level'),
    url(r'^admin/operation/core/book/category/list/$', api.delete_list_category, name='delete-list-category'),
    url(r'^', include(router.urls)),

]
    