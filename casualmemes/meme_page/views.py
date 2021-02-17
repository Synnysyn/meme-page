from django.shortcuts import render
from django.views import View
from .models import *

# Create your views here.


class MenuView(View):
    def get(self, request):
        memes = Meme.objects.all()
        context = {"meme": memes[0]}
        return render(request, "meme_page/menu.html", context)