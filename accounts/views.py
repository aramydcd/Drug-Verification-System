from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, CustomLoginForm
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from drugs.models import Drug
from verification.models import VerificationLog
from django.contrib.auth import get_user_model




User = get_user_model()


@method_decorator(login_required, name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = "accounts/admin_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Statistics
        context["total_users"] = User.objects.count()
        context["total_companies"] = User.objects.filter(role="company").count()
        context["total_drugs"] = Drug.objects.count()
        context["total_verifications"] = VerificationLog.objects.count()

        # Recent logs
        context["recent_logs"] = VerificationLog.objects.select_related("user", "drug").order_by("-timestamp")[:5]

        return context


@method_decorator(login_required, name='dispatch')
class CompanyDashboardView(TemplateView):
    template_name = "accounts/company_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get company drugs
        company_drugs = Drug.objects.filter(company=self.request.user)

        # Stats
        context["total_drugs"] = company_drugs.count()
        context["total_verifications"] = VerificationLog.objects.filter(drug__in=company_drugs).count()

        # Recent verification logs for this company's drugs
        context["recent_logs"] = (
            VerificationLog.objects.select_related("user", "drug")
            .filter(drug__in=company_drugs)
            .order_by("-timestamp")[:5]
        )

        return context




# Create your views here.
def redirect_based_on_role(user):
    """Redirect user to dashboard based on their role."""
    if user.role == "company":
        return redirect("company_dashboard")
    elif user.role == "admin":
        return redirect("admin_dashboard")  # Django admin site
    else:
        return redirect("home")


@login_required
def user_dashboard(request):
    return render(request, "accounts/user_dashboard.html")

@login_required
def company_dashboard(request):
    return render(request, "accounts/company_dashboard.html")

@login_required
def admin_dashboard(request):
    return render(request, "accounts/admin_dashboard.html")

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        return redirect_based_on_role(self.request.user).url


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # 🔒 prevent normal signup as admin
            if user.role == 'admin':
                user.role = 'user'

            user.save()
            return redirect_based_on_role(user)

    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
