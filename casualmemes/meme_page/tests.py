from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
import pytest
from django.contrib.auth.models import User
from meme_page.views import Meme, Genre

# Create your tests here.


def user():
    u = User.objects.create_superuser(
        name="TrollUltimate", password="TrollUltimate123123"
    )
    return u


def genre():
    g = Genre.objects.create(title="casual")
    return g


def meme():
    m = Meme.objects.create(title="kappa", creator=user(), image="")
    m.genres.add(genre())
    return m
