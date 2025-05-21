from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    point = models.IntegerField(validators=[MinValueValidator(1)])
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.point}Pt)"