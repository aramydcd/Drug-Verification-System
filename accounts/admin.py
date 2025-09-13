from django.contrib import admin
from .models import User
from drugs.models import Drug
from verification.models import Verification
from django.utils.html import format_html
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model

# Register your models here.
class MyAdminSite(AdminSite):
    site_header = "💊 Drug Verification Admin"
    site_title = "Drug Verification System"
    index_title = "Admin Dashboard"

    def each_context(self, request):
        context = super().each_context(request)
        User = get_user_model()
        context['total_users'] = User.objects.count()
        context['total_companies'] = User.objects.filter(role='company').count()
        context['total_drugs'] = Drug.objects.count()
        context['total_verifications'] = Verification.objects.count()
        return context


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_number', 'company', 'created_at')
    search_fields = ('name', 'batch_number')
    list_filter = ('company',)


# @admin.register(Verification)
# class VerificationLogAdmin(admin.ModelAdmin):
#     list_display = ('user', 'drug', 'verification_status', 'verification_time')
#     list_filter = ('result',)
#     search_fields = ('drug__name', 'user__username')

#     def verification_status(self, obj):
#         if obj.result:  # or obj.is_valid
#             return format_html('<span style="color:green;font-weight:bold;">Valid</span>')
#         return format_html('<span style="color:red;font-weight:bold;">Fake</span>')
#     verification_status.short_description = "Status"



admin_site = MyAdminSite(name='myadmin')
admin_site.register(User, UserAdmin)
admin_site.register(Drug, DrugAdmin)
admin_site.register(Verification)
