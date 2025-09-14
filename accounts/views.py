from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import  logout
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, CustomLoginForm
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from drugs.models import Drug
from verification.models import Verification
from accounts.models import User
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q



@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # ----------------------------
        # Admin Dashboard
        # ----------------------------
        if user.role == "Admin":
            context["admin_total_users"] = User.objects.count()
            context["admin_total_companies"] = User.objects.filter(role="company").count()
            context["admin_total_drugs"] = Drug.objects.count()
            context["admin_total_verifications"] = Verification.objects.count()

            context["admin_recent_logs"] = (
                Verification.objects.select_related("user", "drug")
                .order_by("-created_at")[:5]
            )

        # ----------------------------
        # Company Dashboard
        # ----------------------------
        elif user.role == "company":
            company_drugs = Drug.objects.filter(company=user)  # user must be a single instance
            context["company_total_drugs"] = company_drugs.count()
            context["company_total_verifications"] = Verification.objects.filter(drug__in=company_drugs).count()

            context["company_recent_logs"] = (
                Verification.objects.select_related("user", "drug")
                .filter(drug__in=company_drugs)
                .order_by("-created_at")[:5]
            )

        # ----------------------------
        # User Dashboard
        # ----------------------------
        elif user.role == "User":
            user_verifications = Verification.objects.filter(user=user)
            context["user_total_verifications"] = user_verifications.count()
            context["user_recent_logs"] = user_verifications.select_related("drug").order_by("-created_at")[:5]

        return context




@method_decorator(login_required, name='dispatch')
class HistoryView(TemplateView):
    template_name = "accounts/history.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get query params
        search_query = self.request.GET.get('q', '')
        result_filter = self.request.GET.get('result', '')  # "authentic" or "fake"

        # Base queryset depending on role
        if user.role == "Admin":
            logs = Verification.objects.select_related("user", "drug").order_by("-created_at")
        elif user.role == "company":
            company_drugs = Drug.objects.filter(company=user)
            logs = Verification.objects.select_related("user", "drug").filter(drug__in=company_drugs).order_by("-created_at")
        else:  # User role
            logs = Verification.objects.select_related("drug").filter(user=user).order_by("-created_at")

        # Apply search filter
        if search_query:
            logs = logs.filter(Q(drug__name__icontains=search_query) | Q(drug__batch_number__icontains=search_query))

        # Apply result filter
        if result_filter == "authentic":
            logs = logs.filter(is_valid=True)
        elif result_filter == "fake":
            logs = logs.filter(is_valid=False)

        # Pagination
        paginator = Paginator(logs, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Add to context
        context["history_logs"] = page_obj
        context["is_paginated"] = page_obj.has_other_pages()
        context["page_obj"] = page_obj
        context["search_query"] = search_query
        context["result_filter"] = result_filter
        context["total_verifications"] = logs.count()

        return context



class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        # Redirect all users to the same dashboard
        return reverse_lazy("dashboard")
    
    

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # 🔒 prevent normal signup as admin
            if user.role == 'admin':
                user.role = 'user'

            user.save()
            return redirect('dashboard')

    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def about_view(request):
    return render(request, 'accounts/about.html')


def home_view(request):
    return render(request, 'home.html')


# @method_decorator(login_required, name='dispatch')
# class HistoryView(TemplateView):
#     template_name = "accounts/history.html"
#     paginate_by = 10

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user

#         # ----------------------------
#         # Admin Dashboard
#         # ----------------------------
#         if user.role == "Admin":
#             context["total_verifications"] = Verification.objects.count()

#             context["history_logs"] = (
#                 Verification.objects.select_related("user", "drug")
#                 .order_by("-created_at")
#             )

#         # ----------------------------
#         # Company Dashboard
#         # ----------------------------
#         elif user.role == "company":
#             company_drugs = Drug.objects.filter(company=user)  # user must be a single instance
#             context["total_verifications"] = Verification.objects.filter(drug__in=company_drugs).count()

#             context["history_logs"] = (
#                 Verification.objects.select_related("user", "drug")
#                 .filter(drug__in=company_drugs)
#                 .order_by("-created_at")
#             )

#         # ----------------------------
#         # User Dashboard
#         # ----------------------------
#         elif user.role == "User":
#             user_verifications = Verification.objects.filter(user=user)
#             context["total_verifications"] = user_verifications.count()
#             context["history_logs"] = user_verifications.select_related("drug").order_by("-created_at")

#         return context
