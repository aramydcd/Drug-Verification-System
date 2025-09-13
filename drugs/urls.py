from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.add_drug, name='add_drug'),
    path('view/', views.view_drugs, name='view_drugs'),
    path("edit/<int:id>/", views.edit_drug, name="edit_drug"),
    path("delete/<int:id>/", views.delete_drug, name="delete_drug"),

]
