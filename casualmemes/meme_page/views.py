from django.shortcuts import render
from django.views import View
from .models import *

# Create your views here.


class MenuView(View):
    def get(self, request):
        
        return render(request, "meme_page/menu.html")