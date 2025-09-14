from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path('about/', views.about_view, name='about'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),

]
