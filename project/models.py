from django.db import models
from django.conf import settings
# Create your models here.

class Project(models.Model):
    AUTH_TYPE_CHOICES = (
        ("email", "Email Based"),
        ("username", "Username Based"),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)
    description = models.TextField()
    auth_type = models.CharField(
        max_length=20,
        choices=AUTH_TYPE_CHOICES,
        default="email"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name