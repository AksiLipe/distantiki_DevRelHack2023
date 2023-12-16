from django.urls import path
from .views import table_view, create_member_view, import_members, index, get_analytics

urlpatterns = [
    path('',  index),
    path('table/', table_view, name='table-view'),
    path('add_member/', create_member_view, name='add-member'),
    path('import_members/', import_members, name='import-members'),
    path('analytics', get_analytics, name='analytics')
]
