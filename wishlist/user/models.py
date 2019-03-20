from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True, validators=[RegexValidator(r'^[a-z0-9_]{4,100}$')])
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    def set_password(self, password):
        super(User, self).set_password(password)

