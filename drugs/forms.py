from django import forms
from .models import Drug
from accounts.models import User   # Import User for company dropdown


class StyledFormMixin:
    """Mixin to add Bootstrap styles to all fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.label


class DrugForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Drug
        fields = ["name", "manufacturer_date", "batch_number", "expiry_date", "description", "image", "company", "qr_code"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Pass logged-in user from view
        super().__init__(*args, **kwargs)

        if user and user.role == "company":
            # Company users: hide company field (auto-assigned in view)
            self.fields.pop("company", None)
        else:
            # Admin: show only users with role = company
            self.fields["company"].queryset = User.objects.filter(role="company")
