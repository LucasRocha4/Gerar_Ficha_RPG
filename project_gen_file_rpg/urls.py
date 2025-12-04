from django.urls import path, include
from app_gen_file_rpg.views import home, criando, lista_mesas, mesa_actions, detalhe_mesa, charsheet, user_registration, password_recover, password_reset_view, password_reset_request, password_reset_confirm_page, password_reset_confirm
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('',                                        home,                                   name='home'),
    path('criando/',                                criando,                                name='criando'),
    path('criando/fichas/',                       charsheet,                               name='charsheet'),
    path('login/',                                  auth_views.LoginView.as_view(),         name='login'),
    path('login/submit/',                           user_registration,                      name='registrar'),
    path('logout/',                                 LogoutView.as_view(next_page='login'),  name='logout'),
    path('password-reset/',                         password_reset_view,                    name='password_reset'),
    path('api/password-reset/',                     password_reset_request,                 name='api_password_reset'),
    path('password-reset/api/password_recover/',    password_recover,                       name='password_recover'),
    path('password-reset-confirm/<uidb64>/<token>/',password_reset_confirm_page,            name='password_reset_confirm_page'),
    path('password-reset-confirm/',                 password_reset_confirm,                 name='password_reset_confirm_api'),
    path('api/token/',                              TokenObtainPairView.as_view(),          name='token'),
    path('api/token/refresh/',                      TokenRefreshView.as_view(),             name='token_refresh'),
    path('mesas/',                                  lista_mesas,                            name='mesas'),
    path('mesas/<int:mesa_id>/',                              detalhe_mesa,                 name='detalhe_mesa'),
    path('mesas/<int:mesa_id>/<str:action>/<int:target_id>/', mesa_actions,                 name='mesa_actions'),
]