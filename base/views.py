from django.shortcuts import render
# from .models import Distance, Time
# from .forms import NameForm, DistanceForm, TimeForm
# from django.shortcuts import redirect
# from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
def index(request):
    return render(request, "base/index.html")
