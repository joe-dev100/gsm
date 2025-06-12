from django.urls import path

from .views import *


app_name="dashboard"

urlpatterns = [
    path("admin/page/", index, name="home_page"),
    path("admin/dashboard/", dashboard_view, name="dashboard_view"),
    path("teller/page/",teller_view, name="teller_page"),
    path("teller/page/cat/<int:pk>",filter_by_category, name="filter_by_category"),
    path("teller/page/search/",search_view, name="search_view"),
    path("teller/page/cat/all/",filter_by_all_category, name="filter_by_all_category"),
    
]