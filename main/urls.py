from django.urls import path
from .views import table_view, create_member_view
from main.views import index

urlpatterns = [
    path('',  index),
    path('table/', table_view, name='table-view'),
    path('add_member/', create_member_view, name='add-member'),
    path('import_member/', create_member_view, name='import-member'),
]