from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager


class User(AbstractUser):
    username = None

    name = models.CharField(
        max_length=7,
        blank=False,
        validators=[MinLengthValidator(2, "이름은 두 글자 이상이여야합니다.")],
    )
    
    email = models.EmailField(
        blank=False,
        unique=True,
        error_messages={"unique":"이미 존재하는 이메일입니다."}
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    is_admin = models.BooleanField(default=False)
    
    birthday = models.DateField(blank=False, null=False)
    
    def __str__(self):
        return self.name