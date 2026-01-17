from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    
    def create_user(self, password=None, **extra_fields):
        if not password:
            raise ValidationError("Users must have a password")

        extra_fields.setdefault("is_active", True)

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(password=password, **extra_fields)
