"""eBook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import views
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='eBook API')

# Register Admin Login Form (Custom)
# AdminSite.login_form = forms.SecureAdminLoginForm

urlpatterns = [
    # url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^', include('core.urls')),


    url(r'^', include('main.urls_api_root')),
    url(r'^api/schema/', schema_view),
    

]

