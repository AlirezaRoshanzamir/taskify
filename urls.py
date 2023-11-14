"""
URL configuration for taskify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from taskify.views import tasks, users

urlpatterns = [
    path("", tasks.search, name="index"),

    path("tasks/", tasks.search, name="tasks"),
    path("tasks/search", tasks.search, name="tasks/search"),
    path("tasks/edit", tasks.edit, name="tasks/edit"),
    path("tasks/create", tasks.create, name="tasks/create"),

    path("users/", users.login_, name="users/login"),
    path("users/login", users.login_, name="users/login"),
    path("users/register", users.register, name="users/register"),
    path("users/logout", users.logout_, name="users/logout"),

    path("admin/", admin.site.urls),
]
