from django import forms
from .models import Profile, Collection, Medicine


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'city', 'date_of_birth']


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['medicine', 'user', 'date']


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'manufacturer', 'cures', 'sideeffects']
