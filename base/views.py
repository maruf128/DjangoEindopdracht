from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required


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
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Gebruiker updated successfully")
            return redirect("user")
    else:
        form = ProfileForm(instance=profile)
    context = {"form": form}
    return render(request, "base/useraanpas.html", context)
