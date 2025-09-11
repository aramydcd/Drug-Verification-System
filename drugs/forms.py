from django import forms
from .models import Drug

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'manufacturer', 'batch_number', 'expiry_date', 'description', 'image']

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
        fields = ["name", "manufacturer", "batch_number", "expiry_date", "description", "image"]
