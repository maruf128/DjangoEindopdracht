from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    path("user/", views.user, name="user"),
    path("edit_user/<int:pk>/", views.edit_user, name="edit_user"),
    path("nieuwe_afhaal/", views.nieuwe_afhaal, name="nieuwe_afhaal"),
    path("nieuwe_medicijn/", views.nieuwe_medicijn, name="nieuwe_medicijn")
]
