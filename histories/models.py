from django.db import models
from django.conf import settings
from actions.models import Action
from rewards.models import Reward
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class ActionHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    point_change = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}が{self.action.name}を実行 (+{self.point_change})"

class RewardHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    point_change = models.IntegerField(validators=[MaxValueValidator(-1)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}が{self.reward.name}を交換 ({self.point_change})"