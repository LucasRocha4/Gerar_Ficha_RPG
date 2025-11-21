from django.urls import path, include
from app_gen_file_rpg.views import home, criando, user_registration
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('',                        home,                           name='home'),
    path('criando/',                criando,                        name='criando'),
    path('login/',                  auth_views.LoginView.as_view(), name='login'),
    path('login/submit/',           user_registration,              name='registration'),
    path('api/token/',              TokenObtainPairView.as_view(),  name='token'),
    path('api/token/refresh/',      TokenRefreshView.as_view(),     name='token_refresh'),
]
