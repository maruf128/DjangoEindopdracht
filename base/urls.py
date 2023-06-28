from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("user/", views.user, name="user"),
    path("edit_user/<int:pk>/", views.edit_user, name="edit_user"),
    path("nieuwe_afhaal/", views.nieuwe_afhaal, name="nieuwe_afhaal"),
    path("afhaal_medicijn/<int:pk>/",
         views.afhaal_medicijn, name="afhaal_medicijn"),
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
    path(
        "medicine/",
        views.medicine,
        name="medicine",
    ),
    path(
        "F/",
        views.collection,
        name="collection",
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
    path(
        "collection/<int:collection_id>/delete/",
        views.collection_delete,
        name="collection_delete",
    ),
    path("password_check/", views.password_check, name="password_check"),
    path(
        "medicijn_gegevens/<int:pk>/",
        views.medicijn_gegevens,
        name="medicijn_gegevens",
    ),
    path(
        "user_collection/<int:pk>/",
        views.user_collection,
        name="user_collection",
    ),
    path(
        "admin_collection_detail/<int:pk>/",
        views.admin_collection_detail,
        name="admin_collection_detail",
    ),
    # path(
    #     "collections/<int:collection_id>/mark_delivered/",
    #     views.mark_delivered,
    #     name="mark_delivered",
    # ),
]
