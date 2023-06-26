from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("user/", views.user, name="user"),
    path("edit_user/<int:pk>/", views.edit_user, name="edit_user"),
    path("nieuwe_afhaal/", views.nieuwe_afhaal, name="nieuwe_afhaal"),
    path("nieuwe_medicijn/", views.nieuwe_medicijn, name="nieuwe_medicijn"),
    path(
        "admin_edit_medicine/<int:pk>/",
        views.admin_edit_medicine,
        name="admin_edit_medicine",
    ),
    path(
        "admin_delete_medicine/<int:pk>/",
        views.admin_delete_medicine,
        name="admin_delete_medicine",
    ),
    path(
        "medicines/",
        views.medicines,
        name="medicines",
    ),
    path("collections/", views.collection_list, name="collection_list"),
    path(
        "collections/<int:collection_id>/",
        views.collection_detail,
        name="collection_detail",
    ),
    path(
        "admin_collection_list/",
        views.admin_collection_list,
        name="admin_collection_list",
    ),
    path(
        "admin_collection_list/<int:collection_id>/",
        views.admin_approve,
        name="admin_approve",
    ),
    path("password_check/", views.password_check, name="password_check"),
    # path(
    #     "collections/<int:collection_id>/mark_delivered/",
    #     views.mark_delivered,
    #     name="mark_delivered",
    # ),
]
