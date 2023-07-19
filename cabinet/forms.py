from django import forms
from django.contrib.auth import get_user_model

from cabinet.models import Task


# from django.contrib.auth.forms import UserCreationForm
# from django.core.exceptions import ValidationError


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["description", "is_completed"]