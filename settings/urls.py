from django.urls import path
from .views import *


app_name="config"

urlpatterns = [
    
    path("settings/",settings_view, name="settings_view"),
    path("settings/email/",mail_settings, name="mail_settings"),
    path("settings/email/<int:pk>",update_user_notification, name="update_user_notification"),
]