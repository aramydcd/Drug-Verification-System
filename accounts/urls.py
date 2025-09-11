from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard, name="accounts_home"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboards
    path("user/dashboard/", views.user_dashboard, name="user_dashboard"),
    path("dashboard/company/", views.CompanyDashboardView.as_view(), name="company_dashboard"),
    # path("company/dashboard/", views.company_dashboard, name="company_dashboard"),
    path("dashboard/admin/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
    # path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),

]
