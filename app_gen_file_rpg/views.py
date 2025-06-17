from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistrarUsuario

class RegistrarUsuario(CreateView):
    form_class = RegistrarUsuario
    template_name = 'registration/registrar.html'
    success_url = reverse_lazy('login')

def home(request):
    return render(request, 'pages/home.html')

def criando(request):
    return render(request, 'pages/criando.html')