from django.contrib import admin
from django.urls import path,include
from . views import *

app_name = 'auth'
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('list/', user_view, name='user_view'),
    path('add/', user_add, name='user_add'),
    path('', login_view, name='login'),
    path('accounts/login/', login_view, name='login'),
    path('forgot-password/', forgot_password_view, name='forgot-password'),
    path('reset-password/<str:token>/', reset_password_view, name='reset-password'),
    path('logout/', logout_view, name='logout'),

    path('edit/<int:pk>/',user_update_view,name="user_update_view"),
    path('delete/<int:pk>/',user_delete_view,name="user_delete_view"),
    path('active/all/',user_active_all_view,name="user_active_all_view"),
    path('deactive/all/',user_deactive_all_view,name="user_deactive_all_view"),
    path('delete/all/',user_delete_all_view,name="user_delete_all_view"),
    path('desactivate/selected/',user_deactivate_selection,name="user_deactivate_selection"),
    path('activate/selected/',user_activate_selection,name="user_activate_selection"),
    path('delete/selected/',user_delete_selection,name="user_delete_selection"),

]