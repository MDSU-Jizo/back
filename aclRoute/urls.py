"""
    AclBundle urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_acl_routes, name='get_acl_routes'),
    path('details/<int:acl_route_id>', views.get_acl_route, name='get_acl_route'),
    path('add', views.add_acl_route, name='add_acl_route'),
    path('update', views.update_acl_route, name='update_acl_route'),
    path('delete/<int:acl_route_id>', views.delete_acl_route, name='delete_acl_route')
]