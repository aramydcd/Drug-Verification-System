from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search-batch/", views.search_by_batch, name="search_by_batch"),
]
