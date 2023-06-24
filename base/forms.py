from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'city', 'date_of_birth']


# class DistanceForm(forms.ModelForm):
#     class Meta:
#         model = Distance
#         fields = ("length", "full_name")

# voorbeelden ^^
