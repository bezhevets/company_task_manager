from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.forms import DateTimeInput, NullBooleanSelect, RadioSelect
from django.utils import timezone

from cabinet.models import Task, Worker


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

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < timezone.now():
            raise ValidationError("The date is incorrect. Date < today's date")
        return deadline


class TaskUpdateForm(forms.ModelForm):

    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = ["description", "is_completed", "priority", "deadline", "assignees"]
        widgets = {
            "deadline": DateTimeInput(attrs={"type": "datetime-local"}),
            "is_completed": NullBooleanSelect(),
            "priority": RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        if not self.user_is_superuser():
            self.fields.pop("deadline")
            self.fields.pop("assignees")

    def user_is_superuser(self):
        user = self.request.user
        return user.is_superuser


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


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search of username worker",
                "style": "width: 400px;"
            }
        )
    )


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ["new_password1", "new_password2"]
