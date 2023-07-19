from django.urls import path

from cabinet.views import TaskListView

urlpatterns = [
    path("", TaskListView.as_view(), name="index"),
]


app_name = "cabinet"
