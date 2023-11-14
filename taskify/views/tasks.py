from typing import Iterable

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse

from taskify.forms import CreateTaskForm, SearchTaskForm, UpdateTaskForm
from taskify.models import Task, TaskStatus


@login_required
def search(request):
    page_number = request.GET.get("page", 1)
    filters = {}
    if request.method == "POST":
        form = SearchTaskForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["id"]:
                filters |= {"id": form.cleaned_data["id"]}
            if form.cleaned_data["name"]:
                filters |= {"name": form.cleaned_data["name"]}
            if form.cleaned_data["status"] in TaskStatus:
                filters |= {"status": form.cleaned_data["status"]}
            if form.cleaned_data["dynamic_fields"]:
                filters |= {
                    "dynamic_fields__contains": form.cleaned_data["dynamic_fields"]
                }
    else:
        form = SearchTaskForm()

    if filters:
        tasks = Task.objects.filter(**filters)
    else:
        print("############################", filters)
        tasks = Task.objects.all()

    page = _paginate_tasks(tasks, page_number)
    return render(request, "tasks/search.html", {"tasks": page, "form": form})


@login_required
def create(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect(reverse("tasks/edit") + "?id={}".format(task.id))
    else:
        form = CreateTaskForm()

    return render(request, "tasks/create.html", {"task": form})


@login_required
def edit(request: HttpRequest):
    task = get_object_or_404(Task, id=request.GET.get("id"))

    if request.method == "GET":
        form = UpdateTaskForm(instance=task)
    elif request.method == "POST":
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            if "delete" in request.POST:
                task.delete()
                return redirect("tasks/search")
            elif "update" in request.POST:
                form.save()

    return render(request, "tasks/edit.html", {"task": form, "id": task.id})


def _paginate_tasks(tasks: Iterable[Task], page_number: int) -> Page[Task]:
    paginator = Paginator(tasks, 10)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
