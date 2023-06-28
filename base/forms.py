from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Profile, Collection, Medicine, User


class ProfileForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Profile
        fields = ["bio", "city", "date_of_birth", "password"]

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.all()
        user_choices = [(user.id, user.username) for user in users]
        self.fields["user"].widget = forms.Select(choices=user_choices)


class TotaalCollectionFrom(forms.ModelForm):
    class Meta:
        model = Collection
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.all()
        user_choices = [(user.id, user.username) for user in users]
        self.fields["user"].widget = forms.Select(choices=user_choices)


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["name", "manufacturer", "cures", "sideeffects"]


class MedicineEditForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["name", "manufacturer", "cures", "sideeffects"]


class CollectionDetailForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["collected"]


class AdminApproveForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["collectedapproved"]


class PasswordCheckForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
