from django.shortcuts import render
# from .models import Distance, Time
# from .forms import NameForm, DistanceForm, TimeForm
from django.shortcuts import redirect
# from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
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
