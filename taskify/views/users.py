from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from taskify.forms import LoginForm, RegisterForm


def login_(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next = request.GET.get("next", "index")
                return redirect(next)
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users/login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def logout_(request):
    logout(request)
    return redirect("users/login")
