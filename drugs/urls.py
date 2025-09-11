from django.urls import path
from .views import add_drug, view_drugs, edit_drug, delete_drug

urlpatterns = [
    path('add/', add_drug, name='add_drug'),
    path('view/', view_drugs, name='view_drugs'),
    path('edit/<int:pk>/', edit_drug, name='edit_drug'),
    path("delete/<int:pk>/", delete_drug, name="delete_drug"),

]



# urlpatterns = [
#     path("add/", views.add_drug, name="add_drug"),
#     path("view/", views.view_drugs, name="view_drugs"),
#     path("edit/<int:drug_id>/", views.edit_drug, name="edit_drug"),
#     path("delete/<int:drug_id>/", views.delete_drug, name="delete_drug"),
# ]
