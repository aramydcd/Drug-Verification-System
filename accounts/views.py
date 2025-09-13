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
        elif user.role == "Company":
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

def history_view(request):
    return render(request, 'accounts/history.html')

def home_view(request):
    return render(request, 'home.html')
