"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from user.views import login, register

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^accounts/login/", login, name="login"),
    re_path(r"^accounts/register/", register, name="register"),
    path('user/', include('user.urls'), name="user_"),
    path('level/', include('level.urls'), name="level_"),
    path('type/', include('type.urls'), name="type_"),
    path('role/', include('role.urls'), name="role_"),
    path('acl-bundle/', include('aclBundle.urls'), name="acl_bundle_"),
    path('acl-route/', include('aclRoute.urls'), name="acl_route_"),
    path('interest/', include('interest.urls'), name="interest_"),
    path('language/', include('language.urls'), name="language_"),
    path('itinerary/', include('itinerary.urls'), name="itinerary_"),
]
