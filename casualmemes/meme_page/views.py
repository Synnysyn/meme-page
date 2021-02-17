from django.shortcuts import render, redirect
from django.db.models import query
from django.views import View
from django.views.generic import FormView, CreateView, UpdateView, DeleteView, ListView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.


class MenuView(View):
    def get(self, request):
        memes = Meme.objects.all()
        context = {"meme": memes[0]}
        return render(request, "meme_page/menu.html", context)


class MemeCreateView(PermissionRequiredMixin, View):
    permission_required = "meme_page.add_meme"

    def get(self, request):
        form = CreateMemeForm()
        ctx = {"form":form}
        return render(request, "meme_page/meme_create.html", ctx)
    
    def post(self, request):
        form = CreateMemeForm(request.POST, request.FILES)
        if form.is_valid():
            meme = Meme.objects.create(title=form.cleaned_data["title"], image=form.cleaned_data["image"], creator=request.user)
            meme.genres.set(form.cleaned_data["genres"])
            meme.save()
            return redirect("index")
        ctx = {"form":form}
        return render(request, "meme_page/meme_create.html", ctx)



    # form_class = CreateMemeForm
    # template_name = "meme_page/meme_create.html"
    # success_url = reverse_lazy("index")

    # def form_valid(self, form):
    #     meme = form.save()
    #     return super().form_valid(form)