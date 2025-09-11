
from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    ROLE_CHOICES = [('Admin', 'Admin'), 
                    ('User', 'User'),
                    ("company", "Company")
                    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='User'
    )
    

    def __str__(self):
        return self.username


