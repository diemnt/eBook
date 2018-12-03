from rest_framework import routers
from django.conf.urls import url, include
from personal import api_viewset, api


router = routers.DefaultRouter()
router.register(r'admin/operation/personal/package',
                api_viewset.PackageViewSet)
router.register(r'admin/operation/personal', api_viewset.PersonalViewSet)

urlpatterns = [
    url(r'^admin/operation/personal/package/(?P<package_id>[0-9]+)/state/$',
        api.change_package_state, name='change-personal-package-state'),
    url(r'^', include(router.urls)),


    url(r'^personal/login/', include('rest_social_auth.urls_jwt')),

]
