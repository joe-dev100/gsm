from django.urls import path

from .views import *


app_name="facture"

urlpatterns = [
    path("list/", list_facture, name="facture_list"), 
    path("details/<int:pk>/", facture_details, name="facture_details"),
    path("delete/<int:pk>/", delete_facture, name="facture_delete"),
    path("filter_by_date/", filter_facture_by_date, name="filter_facture_by_date"),
]