from django.shortcuts import render
from .models import Profile, Medicine, User, Collection
from .forms import ProfileForm, CollectionForm, MedicineForm, AdminApproveForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
def index(request):
    return render(request, "base/index.html")


# registratie en login view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    context = {"form": form}
    return render(request, "registration/register.html", context)


@login_required
def user(request):
    # pak de user en vraag dan zijn gegevens
    ingelogde = request.user
    gegevens = Profile.objects.filter(user=ingelogde)
    context = {"gegevens": gegevens, "naam": ingelogde}
    return render(request, "base/user.html", context)


@login_required
def edit_user(request, pk):
    profile = Profile.objects.get(pk=pk)
    user = profile.user

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Jouw gegevens zijn aangepast")
            return redirect("user")
    else:
        form = ProfileForm(instance=profile)

    context = {"form": form}
    return render(request, "base/useraanpas.html", context)


@login_required
def collection_list(request):
    collections = Collection.objects.filter(user=request.user, collectedapproved=False)

    context = {"collections": collections}
    return render(request, "base/collection_list.html", context)


@staff_member_required
def admin_collection_list(request):
    collections = Collection.objects.filter(collectedapproved=False)

    context = {"collections": collections}
    return render(request, "base/admin_collection_list.html", context)


@staff_member_required
def admin_approve(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)

    if request.method == "POST":
        form = AdminApproveForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            # Handle form submission success
    else:
        form = AdminApproveForm(instance=collection)

    context = {
        "collection": collection,
        "form": form,
    }
    return render(request, "base/collection_detail.html", context)


# @login_required
# def collection_detail(request, collection_id):
#     collection = get_object_or_404(Collection, id=collection_id, user=request.user)

#     if request.method == "POST" and "delivered" in request.POST:
#         collection.collected_approved = True
#         collection.collected_approved_by = request.user
#         collection.save()
#         # Redirect or display success message

#     context = {"collection": collection}
#     return render(request, "base/collection_detail.html", context)


@staff_member_required
def nieuwe_afhaal(request):
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nieuwe afhaal actie toegevoegd")
            return redirect("user")
    else:
        form = CollectionForm()
    context = {"form": form}
    return render(request, "base/afhaalform.html", context)


@staff_member_required
def nieuwe_medicijn(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        name = request.POST.get("name")
        does_medicine_exist = Medicine.objects.filter(name=name).exists()
        if does_medicine_exist:
            form.add_error("name", "deze medicijn bestaat al")
        if form.is_valid():
            form.save()
            messages.success(request, "nieuwe medicijn toegevoegd")
            return redirect("user")
    else:
        form = MedicineForm()
    context = {"form": form}
    return render(request, "base/medicijnform.html", context)


from .forms import CollectionDetailForm


@login_required
def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id, user=request.user)

    if request.method == "POST":
        form = CollectionDetailForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            # Handle form submission success
    else:
        form = CollectionDetailForm(instance=collection)

    context = {
        "collection": collection,
        "form": form,
    }
    return render(request, "base/collection_detail.html", context)
