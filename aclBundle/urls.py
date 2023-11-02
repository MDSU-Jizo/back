"""
    AclBundle urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_acl_bundles, name='get_acl_bundles'),
    path('details/<int:acl_bundle_id>', views.get_acl_bundle, name='get_acl_bundle'),
    path('add', views.add_acl_bundle, name='add_acl_bundle'),
    path('update', views.update_acl_bundle, name='update_acl_bundle'),
    path('delete/<int:acl_bundle_id>', views.delete_acl_bundle, name='delete_acl_bundle')
]