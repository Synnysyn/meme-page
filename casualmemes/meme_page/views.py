from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.db.models import query
from django.views import View
from django.views.generic import FormView, CreateView, UpdateView, DeleteView, ListView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django import forms
import random


# Create your views here.


class MenuView(View):
    def get(self, request):
        memes = Meme.objects.all().order_by("-pk")
        context = {"memes": []}
        for meme in memes:
            avatar = Avatar.objects.filter(owner=meme.creator)
            try:
                avatar = avatar[0]
            except IndexError:
                avatar = "static_avatar"
            clean_reactions = [
                f"{REACTIONS[0][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[0][0]).count()}",
                f"{REACTIONS[1][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[1][0]).count()}",
                f"{REACTIONS[2][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[2][0]).count()}",
                f"{REACTIONS[3][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[3][0]).count()}",
                ]
            
            context["memes"].append({
                "avatar":avatar,
                "clean_reactions":clean_reactions,
                "meme":meme,
            })
        return render(request, "meme_page/menu.html", context)


class MemeCreateView(PermissionRequiredMixin, View):
    permission_required = "meme_page.add_meme"

    def get(self, request):
        form = CreateMemeForm()
        ctx = {"form": form}
        return render(request, "meme_page/meme_create.html", ctx)

    def post(self, request):
        form = CreateMemeForm(request.POST, request.FILES)
        if form.is_valid():
            meme = Meme.objects.create(
                title=form.cleaned_data["title"],
                image=form.cleaned_data["image"],
                creator=request.user,
            )
            meme.genres.set(form.cleaned_data["genres"])
            meme.save()
            return redirect("index")
        ctx = {"form": form}
        return render(request, "meme_page/meme_create.html", ctx)


class AddUserView(FormView):
    form_class = AddUserForm
    template_name = "meme_page/user_add.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data["password"])
        user.save()
        group = Group.objects.get(name="Any User")
        group.user_set.add(user)
        return super().form_valid(form)
