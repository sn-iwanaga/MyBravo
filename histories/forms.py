from django import forms
from django.forms import DateTimeInput
from django.utils import timezone

from .models import ActionHistory, RewardHistory
from actions.models import Action
from rewards.models import Reward

class ActionHistoryForm(forms.ModelForm):
    action = forms.ModelChoiceField(
        queryset=Action.objects.none(),
        label='アクション'
    )
    created_at = forms.DateTimeField(
        label='日時',
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = ActionHistory
        fields = ['action', 'created_at']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action'].queryset = Action.objects.filter(user=user, is_deleted=False)

    def clean_created_at(self):
        input_dt = self.cleaned_data['created_at']
        if input_dt > timezone.now():
            raise forms.ValidationError("未来の日付は指定できません。")
        return input_dt


class RewardHistoryForm(forms.ModelForm):
    reward = forms.ModelChoiceField(
        queryset=Reward.objects.none(),
        label='ご褒美'
    )
    created_at = forms.DateTimeField(
        label='日時',
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = RewardHistory
        fields = ['reward', 'created_at']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reward'].queryset = Reward.objects.filter(user=user, is_deleted=False)

    def clean_created_at(self):
        input_dt = self.cleaned_data['created_at']
        if input_dt > timezone.now():
            raise forms.ValidationError("未来の日付は指定できません。")
        return input_dt