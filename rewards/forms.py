from django import forms
from .models import Reward

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ('name', 'point')