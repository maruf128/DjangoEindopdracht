from .forms import CollectionDetailForm
from django.shortcuts import render
from .models import Profile, Medicine, User, Collection
from .forms import (
    ProfileForm,
    CollectionForm,
    MedicineForm,
    AdminApproveForm,
    PasswordCheckForm,
    MedicineEditForm,
)
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate

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
def password_check(request):
    if request.method == "POST":
        form = PasswordCheckForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user = authenticate(username=request.user.username, password=password)
            if user is not None and user == request.user:
                return redirect("edit_user", pk=request.user.pk)
            else:
                form.add_error("password", "Invalid password")
    else:
        form = PasswordCheckForm()

    context = {"form": form}
    return render(request, "base/password_check.html", context)


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
def medicine(request):
    return render(request, "base/medicine.html")


@staff_member_required
def collection(request):
    return render(request, "base/collection.html")


@staff_member_required
def collection_delete(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    if request.method == "POST":
        collection.delete()
        return render(request, "base/collection.html")
    context = {
        "collection": collection,
    }
    return render(request, "collection_delete.html", context)


@staff_member_required
def admin_approve(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)

    if request.method == "POST":
        form = AdminApproveForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
    else:
        form = AdminApproveForm(instance=collection)

    context = {
        "collection": collection,
        "form": form,
    }
    return render(request, "base/collection.html", context)


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


@staff_member_required
def medicines(request):
    medicines = Medicine.objects.filter()

    context = {"medicines": medicines}
    return render(request, "base/medicines.html", context)


@staff_member_required
def admin_edit_medicine(request, pk):
    medicine = Medicine.objects.get(pk=pk)

    if request.method == "POST":
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicijn gegevens aangepast.")
            return redirect("user")
    else:
        form = MedicineForm(instance=medicine)

    # Add 'medicine' to the context
    context = {"form": form, "medicine": medicine}
    return render(request, "base/admin_edit_medicine.html", context)


@staff_member_required
def admin_delete_medicine(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    medicine.delete()
    messages.success(request, "Medicine deleted successfully.")
    return redirect("user")


@staff_member_required
def nieuwe_afhaal(request):
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            # krijg de data uit de formulier
            user = form.cleaned_data.get('user')
            date = form.cleaned_data.get('date')
            medicijn = form.cleaned_data.get('medicine')
            # kijk of er al een collectie voor bestaat
            existing_collection = Collection.objects.filter(user=user, date=date, medicine=medicijn).exists()
            if existing_collection:
                messages.error(request, "Er bestaat al een afhaal actie voor de gebruiker op de opgegeven datum.")
                return redirect("user")
            else:
                form.save()
                messages.success(request, "Nieuwe afhaal actie toegevoegd")
                return redirect("user")
    else:
        form = CollectionForm()
    context = {"form": form}
    return render(request, "base/afhaalform.html", context)


@staff_member_required
def afhaal_medicijn(request, pk):
    # krijg de medicine, 404 gekregen van gpt zorgt ervoor dat
    # er een error komt zodra de medicijn niet gevonden word
    medicine = get_object_or_404(Medicine, id=pk)
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            # krijg de data uit de tabel
            user = form.cleaned_data.get('user')
            date = form.cleaned_data.get('date')
            # kijk of het bestaat
            existing_collection = Collection.objects.filter(user=user,
                                                            date=date,
                                                            medicine=medicine).exists()
            if existing_collection:
                messages.error(request, "Er bestaat al een afhaal actie voor de gebruiker op de opgegeven datum.")
                return redirect("user")
            else:
                form.save()
                messages.success(request, "Nieuwe afhaal actie toegevoegd")
                return redirect("user")
    else:
        # anders maak je de formulier met de gegeven medicijn
        initial_data = {'medicine': medicine.name}
        form = CollectionForm(initial=initial_data)
    context = {"form": form, "medicijn": medicine.name}
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


@login_required
def medicijn_gegevens(request, name):
    ingelogde = request.user
    gegevens = Medicine.objects.filter(name=name)
    collection_count = Collection.objects.filter(
        user=ingelogde, medicine__name=name, collected=True
    ).count()
    context = {
        "gegevens": gegevens,
        "naam": ingelogde,
        "collection_count": collection_count,
    }
    return render(request, "base/medicijn_detail.html", context)
