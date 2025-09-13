from django.db import models
from django.conf import settings
from drugs.models import Drug
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class VerificationLog(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    verification_time = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=50)  # valid, expired, counterfeit

    def __str__(self):
        return f"{self.drug.name} - {self.result}"
    
class Verification(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_valid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification for {self.drug.name} - {'Valid' if self.is_valid else 'Fake'}"
