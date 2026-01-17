from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from .manager import UserManager
from project.models import Project

# Create your models here.
  
class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True
    )
    password = models.CharField(max_length=128)
    user_data = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        if self.username:
            return self.username
        if self.email:
            return self.email
        return f"User {self.pk}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    

class ProjectUserMapping(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    mapped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user} in {self.project}"
    
    def clean(self):
        if self.project.auth_type == "email" and not self.user.email:
            raise ValidationError("Project requires email-based users.")

        if self.project.auth_type == "username" and not self.user.username:
            raise ValidationError("Project requires username-based users.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)