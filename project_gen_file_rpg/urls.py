from django.urls import path, include
from app_gen_file_rpg.views import home, criando
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('criando/', criando, name='criando'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
