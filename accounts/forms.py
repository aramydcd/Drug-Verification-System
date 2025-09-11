from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class StyledFormMixin:
    """Mixin to add Bootstrap styles to all fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.label

class SignUpForm(StyledFormMixin, UserCreationForm):
    role = forms.ChoiceField(choices=[('Admin', 'Admin'), 
                    ('User', 'User'),
                    ("company", "Company")
                    ], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

class LoginForm(StyledFormMixin,AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class CustomLoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.label
