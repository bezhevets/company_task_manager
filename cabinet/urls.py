from django.contrib.auth.views import PasswordChangeView
from django.urls import path

from cabinet.views import (
    index,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDetailView,
    TaskDeleteView,
    WorkerCreateView,
    WorkerDetailView,
    WorkerUpdateView,
    password_change,
    TaskCompletedView,
    TaskAddOrDelWorkerView,
    WorkerListView, WorkerDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path(
        "task/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "task/<int:pk>/detail/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "task/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "task/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "task/<int:pk>/task_completed/",
        TaskCompletedView.as_view(),
        name="task-completed"
    ),
    path(
        "task/<int:pk>/add_or_del_worker/",
        TaskAddOrDelWorkerView.as_view(),
        name="task-add-or-del-worker"
    ),
    path(
        "worker/create/",
        WorkerCreateView.as_view(),
        name="worker-create"
    ),
    path(
        "worker/<int:pk>/profile/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "worker/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "worker/community/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
    path(
        "worker/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path(
        "change-password/",
        password_change,
        name="change-password"
    ),
]


app_name = "cabinet"
