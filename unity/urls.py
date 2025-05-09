from .views import *
from django.urls import path
app_name = 'unity'
urlpatterns = [
    path('list/',unity_view,name="unity_list_view"),
    path('edit/<int:pk>/',unity_update_view,name="unity_update_view"),
    path('delete/<int:pk>/',unity_delete_view,name="unity_delete_view"),
    path('add/',unity_add_view,name="unity_add_view"),
    path('active/all/',unity_active_all_view,name="unity_active_all_view"),
    path('deactive/all/',unity_deactive_all_view,name="unity_deactive_all_view"),
    path('delete/all/',unity_delete_all_view,name="unity_delete_all_view"),
    path('desactivate/selected/',unity_deactivate_selection,name="unity_deactivate_selection"),
    path('activate/selected/',unity_activate_selection,name="unity_activate_selection"),
    path('delete/selected/',unity_delete_selection,name="unity_delete_selection"),
    
]