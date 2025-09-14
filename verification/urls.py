from django.urls import path
from . import views

urlpatterns = [
    path("search-batch/", views.search_by_batch, name="search_by_batch"),
    path("search-qr/", views.search_by_qr_code, name="search_by_qr_code"),
]
