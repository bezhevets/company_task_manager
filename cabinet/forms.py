from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.forms import DateTimeInput, Select, NullBooleanSelect, RadioSelect

from cabinet.models import Task, Worker


# from django.contrib.auth.forms import UserCreationForm
# from django.core.exceptions import ValidationError

class TaskCreateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": DateTimeInput(attrs={"type": "datetime-local"}),
            "is_completed": NullBooleanSelect(),
            "priority": RadioSelect()
        }


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["description", "is_completed"]


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search of name task",
                "style": "width: 400px;"
            }
        )
    )


class WorkerCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ["new_password1", "new_password2"]
