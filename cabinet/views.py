from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from cabinet.forms import TaskSearchForm, TaskCreateForm, WorkerCreateForm, ChangePasswordForm, WorkerSearchForm
from cabinet.models import Task, Worker


@login_required
def index(request) -> str:
    all_task = Task.objects.all()

    not_completed_task = all_task.filter(is_completed=False)
    num_not_completed_task = not_completed_task.count()
    last_task = all_task.first()

    tasks_for_user = all_task.filter(assignees=request.user.id)
    tasks_for_user_completed = tasks_for_user.filter(is_completed=True)

    context = {
        "num_not_completed_task": num_not_completed_task,
        "last_task": last_task,
        "not_completed_task": not_completed_task,
        "tasks_for_user": tasks_for_user,
        "tasks_for_user_completed": tasks_for_user_completed,
    }

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
        queryset = (Task.objects.all().select_related("task_type")
                    .prefetch_related("assignees").order_by(F("is_completed"), F("deadline")))
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
    queryset = Task.objects.all().select_related("task_type").prefetch_related("assignees")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ["description", "is_completed"]
    success_url = reverse_lazy("cabinet:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("cabinet:task-list")


class TaskCompletedView(LoginRequiredMixin, generic.View):
    model = Task
    fields = ("is_completed",)

    def post(self, request, pk):
        task = Task.objects.get(id=pk)

        if task.is_completed is False:
            task.is_completed = True
            task.save()

        return redirect("cabinet:index")


class TaskAddOrDelWorkerView(LoginRequiredMixin, generic.View):
    model = Task
    fields = ("assignees",)

    def post(self, request, pk):
        user = request.user
        task = Task.objects.get(id=pk)

        if user in task.assignees.all():
            task.assignees.remove(user)
        else:
            task.assignees.add(user)

        return redirect("cabinet:task-list")


def is_admin(user):
    return user.is_superuser


class WorkerCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm

    def test_func(self):
        return is_admin(self.request.user)


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("workers__task_type")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "email"]

    def get_success_url(self) -> str:
        return reverse_lazy("cabinet:worker-detail", kwargs={"pk": self.object.pk})


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "cabinet/worker_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = WorkerSearchForm(initial={"username": username})

        return context

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = WorkerSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return queryset


@login_required
def password_change(request) -> str:
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect("login")
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    form = ChangePasswordForm(user)
    return render(request, 'cabinet/change_password.html', {'form': form})
