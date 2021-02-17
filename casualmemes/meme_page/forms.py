from .models import *
from django import forms
from django.contrib.auth.models import User


class CreateMemeForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = [
            "title",
            "image",
            "genres",
        ]
        widgets = {"genres": forms.CheckboxSelectMultiple}
