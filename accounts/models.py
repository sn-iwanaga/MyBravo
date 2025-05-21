from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

# カスタムユーザモデル
class User(AbstractUser):
    point = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.username