from .models import *
from django import forms
from django.contrib.auth.models import User


class CreateMemeForm(forms.ModelForm):
    """
    use it to crete new meme
    """
    class Meta:
        model = Meme
        fields = [
            "title",
            "image",
            "genres",
        ]
        widgets = {"genres": forms.CheckboxSelectMultiple}


class AddUserForm(forms.ModelForm):
    """
    use it to add new user
    """
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "repeat_password",
            "email",
        ]
        widgets = {"password": forms.PasswordInput}

    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")
        if password != repeat_password:
            msg = "Passwords must be the same"
            self.add_error("password", msg)
            self.add_error("repeat_password", msg)


class AvatarChange(forms.ModelForm):
    """
    use it to change or add avatar
    """
    class Meta:
        model = Avatar
        fields = ["image"]
