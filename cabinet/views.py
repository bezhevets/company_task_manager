from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from cabinet.models import Task


# Create your views here.


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.all().select_related("task_type").prefetch_related("assignees__workers")
    template_name = "cabinet/task_list.html"
    context_object_name = "task_list"


class TaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("cabinet:task-list")
