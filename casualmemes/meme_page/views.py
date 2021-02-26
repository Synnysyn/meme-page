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
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random


# Create your views here.


class MenuView(View):
    def get(self, request):
        memes = Meme.objects.all().order_by("-pk")
        genres = Genre.objects.all()
        clean_memes = []

        for meme in memes:
            avatar = Avatar.objects.filter(owner=meme.creator)
            try:
                avatar = avatar[0]
            except IndexError:
                avatar = "static_avatar"
            clean_reactions = [
                [
                    f"{REACTIONS[0][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[0][0]).count()}",
                    REACTIONS[0][1],
                ],
                [
                    f"{REACTIONS[1][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[1][0]).count()}",
                    REACTIONS[1][1],
                ],
                [
                    f"{REACTIONS[2][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[2][0]).count()}",
                    REACTIONS[2][1],
                ],
                [
                    f"{REACTIONS[3][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[3][0]).count()}",
                    REACTIONS[3][1],
                ],
            ]

            clean_memes.append(
                {
                    "avatar": avatar,
                    "clean_reactions": clean_reactions,
                    "meme": meme,
                }
            )
        
        page = request.GET.get('page', 1)
        paginator = Paginator(clean_memes,5)

        try:
            dict_memes = paginator.page(page)
        except PageNotAnInteger:
            dict_memes = paginator.page(1)
        except EmptyPage:
            dict_memes = paginator.page(paginator.num_pages)

        context = {
            'dict_memes': dict_memes,
            'genres': genres,
        }

        return render(request, "meme_page/menu.html", context)

    def post(self, request):
        if "react_meme_id" in request.POST:
            meme = Meme.objects.get(pk=request.POST.get("react_meme_id"))
            if REACTIONS[0][1] in request.POST:
                reaction = REACTIONS[0][0]
            elif REACTIONS[1][1] in request.POST:
                reaction = REACTIONS[1][0]
            elif REACTIONS[2][1] in request.POST:
                reaction = REACTIONS[2][0]
            elif REACTIONS[3][1] in request.POST:
                reaction = REACTIONS[3][0]
            try:
                react = Reaction.objects.get(
                    reaction_from=request.user, reaction_to=meme
                )
                react = Reaction.objects.filter(
                    reaction_from=request.user, reaction_to=meme
                )
                react.delete()
            except MultipleObjectsReturned:
                react = Reaction.objects.filter(
                    reaction_from=request.user, reaction_to=meme
                )
                react.delete()
            except ObjectDoesNotExist:
                pass
            react = Reaction.objects.create(
                reaction_from=request.user, reaction_to=meme, reaction=reaction
            )
            url = f"/?page={request.GET.get('page', 1)}#meme{meme.pk}"
            return redirect(url)


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


class CreateReportView(FormView):
    def get(self, request, report_id):
        ctx = {"report_id": report_id}
        return render(request, "meme_page/report_create.html", ctx)

    def post(self, request, report_id):
        message = request.POST["report_message"]
        reported_meme = Meme.objects.get(pk=report_id)
        Report.objects.create(message=message, reported=reported_meme)
        return redirect("index")

class AvatarChangeView(FormView):
    def get(self, request):
        form = AvatarChange()
        ctx = {"form": form}
        return render(request, "meme_page/avatar_form.html", ctx)

    def post(self, request):
        form = AvatarChange(request.POST, request.FILES)
        if form.is_valid():
            old_avatars = Avatar.objects.filter(owner=request.user)
            old_avatars.delete()
            Avatar.objects.create(
                image=form.cleaned_data["image"],
                owner=request.user,
            )
            return redirect("index")
        ctx = {"form": form}
        return render(request, "meme_page/avatar_form.html", ctx)