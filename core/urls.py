from django.conf.urls import url, include
from core import views

urlpatterns = [
    url(r'^media/$', views.media_access, name='media')
]