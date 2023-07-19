from django.urls import path

from cabinet.views import TaskListView, TaskCreateView

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
]


app_name = "cabinet"
