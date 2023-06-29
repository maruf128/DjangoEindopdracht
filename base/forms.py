from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Profile, Collection, Medicine, User
from django.utils import timezone


class ProfileForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Profile
        fields = ["bio", "city", "date_of_birth", "password"]
        labels = {
            "bio": "Bio",
            "city": "Stad",
            "date_of_birth": "Geboortedatum",
            "password": "Wachtwoord",
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            profile.user.set_password(password)
        if commit:
            profile.user.save()
            profile.save()
        return profile


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["medicine", "user", "date"]
        labels = {"medicine": "Medicijn", "user": "Patient", "date": "Datum"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        medicines = Medicine.objects.all()
        medicine_choices = [(None, "-----")] + [
            (medicine.id, medicine.name) for medicine in medicines
        ]
        self.fields["medicine"].widget = forms.Select(choices=medicine_choices)
        users = User.objects.all()
        user_choices = [(None, "-----")] + [(user.id, user.username) for user in users]
        self.fields["user"].widget = forms.Select(choices=user_choices)

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date < timezone.now().date():
            raise forms.ValidationError(
                "De datum moet gelijk zijn aan of later zijn dan vandaag."
            )
        return date


class CollectionFormMedicine(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["user", "date"]
        labels = {"user": "Patient", "date": "Datum"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.all()
        user_choices = [(None, "-----")] + [(user.id, user.username) for user in users]
        self.fields["user"].widget = forms.Select(choices=user_choices)

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date is not None and date < timezone.now().date():
            raise forms.ValidationError(
                "De datum moet gelijk zijn aan of later zijn dan vandaag."
            )
        return date


class TotaalCollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            "medicine",
            "user",
            "date",
            "collected",
            "collectedapproved",
            "collectedapprovedby",
        ]
        labels = {
            "medicine": "Medicijn",
            "user": "Patient",
            "date": "Datum",
            "collected": "Afgehaald",
            "collectedapproved": "Afhaling controle",
            "collectedapprovedby": "Afhaling controle door",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        medicines = Medicine.objects.all()
        medicine_choices = [(None, "-----")] + [
            (medicine.id, medicine.name) for medicine in medicines
        ]
        self.fields["medicine"].widget = forms.Select(choices=medicine_choices)
        users = User.objects.all()
        user_choices = [(None, "-----")] + [(user.id, user.username) for user in users]
        self.fields["user"].widget = forms.Select(choices=user_choices)

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date is not None and date < timezone.now().date():
            raise forms.ValidationError(
                "De datum moet gelijk zijn aan of later zijn dan vandaag."
            )
        return date


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["name", "manufacturer", "cures", "sideeffects"]
        labels = {
            "name": "Naam",
            "manufacturer": "Fabrikant",
            "cures": "Genezingen",
            "sideeffects": "Bijwerkingen",
        }


class MedicineEditForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["name", "manufacturer", "cures", "sideeffects"]
        labels = {
            "name": "Naam",
            "manufacturer": "Fabrikant",
            "cures": "Genezingen",
            "sideeffects": "Bijwerkingen",
        }


class CollectionDetailForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["collected"]
        labels = {"collected": "Afhaling"}


class AdminApproveForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["collectedapproved"]
        labels = {"collectedapproved": "Afhaling controle"}


class PasswordCheckForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
