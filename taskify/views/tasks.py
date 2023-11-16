from typing import Iterable

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render, reverse

from taskify.forms import CreateTaskForm, SearchTaskForm, UpdateTaskForm
from taskify.models import Task, TaskStatus


@login_required
def search(request):
    page_number = request.GET.get("page", 1)
    filters = {}
    if request.method == "POST":
        search_form = SearchTaskForm(request.POST)
        if search_form.is_valid():
            if search_form.cleaned_data["id"]:
                filters |= {"id": search_form.cleaned_data["id"]}
            if search_form.cleaned_data["name"]:
                filters |= {"name": search_form.cleaned_data["name"]}
            if search_form.cleaned_data["status"] in TaskStatus:
                filters |= {"status": search_form.cleaned_data["status"]}
            if search_form.cleaned_data["dynamic_fields"]:
                filters |= {
                    "dynamic_fields__contains": search_form.cleaned_data[
                        "dynamic_fields"
                    ]
                }
    else:
        search_form = SearchTaskForm()

    if filters:
        tasks = Task.objects.filter(**filters)
    else:
        tasks = Task.objects.all()

    page_object = _paginate_tasks(tasks, page_number)
    elided_page_range = page_object.paginator.get_elided_page_range(page_object.number)

    return render(
        request,
        "tasks/search.html",
        {
            "page_object": page_object,
            "elided_page_range": elided_page_range,
            "search_form": search_form,
        },
    )


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
