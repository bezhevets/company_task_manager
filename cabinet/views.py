from django.shortcuts import render
from django.views import generic

from cabinet.models import Task


# Create your views here.


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.all().select_related("task_type").prefetch_related("workers")
    template_name = "cabinet/index.html"
    context_object_name = "task_list"
