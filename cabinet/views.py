from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from cabinet.forms import TaskSearchForm, TaskCreateForm
from cabinet.models import Task


@login_required
def index(request) -> str:
    all_task = Task.objects.all()

    not_completed_task = all_task.filter(is_completed=False)
    num_not_completed_task = not_completed_task.count()
    last_task = all_task.first()

    context = {
        "num_not_completed_task": num_not_completed_task,
        "last_task": last_task,
        "all_task": all_task,
        "not_completed_task": not_completed_task,
    }
    print(request.user.id)

    return render(request, "cabinet/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "cabinet/task_list.html"
    context_object_name = "task_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        queryset = Task.objects.all().select_related("task_type").prefetch_related("assignees__workers")
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("cabinet:task-list")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ["description", "is_completed"]
    success_url = reverse_lazy("cabinet:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("cabinet:task-list")
