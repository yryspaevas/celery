from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string

from .tasks import send_activation_code

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **kwargs):
        assert email, "Email is required"
        email = self.normalize_email(email)
        user:User = self.model(email=email, **kwargs)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        send_activation_code.delay(user.email, user.activation_code)
        return user


    def create_superuser(self, email, password, **kwargs):
        assert email,  "Email is required"
        kwargs['is_active'] = True
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        email = self.normalize_email(email)
        user:User = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user




class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def create_activation_code(self):
        self.activation_code = get_random_string(8, 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM123456789')

