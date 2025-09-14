from django.conf import settings
from django.db import models

# Create your models here.

class Drug(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    batch_number = models.CharField(max_length=100, unique=True)
    manufacturer_date = models.CharField(max_length=255)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="drugs/images/", blank=True, null=True)
    qr_code = models.CharField(max_length=255, unique=True)


    # 🔑 NEW: Link to company (User with role="company")
    company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="drugs"
    )

    def __str__(self):
        return f"{self.name} ({self.batch_number})"
