from django.urls import path, include
from app_gen_file_rpg.views import (
    home,           # Landing Page
    selecao,        # Antiga Home (Seleção de Personagem) - Agora view 'selecao' no views.py
    criando, 
    feedback, 
    lista_mesas, 
    mesa_actions, 
    detalhe_mesa, 
    charsheet, 
    user_registration, 
    password_recover, 
    password_reset_view, 
    password_reset_request, 
    password_reset_confirm_page, 
    password_reset_confirm
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 1. Landing Page (Página Inicial Visual)
    path('', home, name='home'), 
    
    # 2. Seleção de Personagem (Antiga Home)
    path('nova-ficha/', selecao, name='selecao'), # Mudei para 'nova-ficha/' para ser mais amigável

    # 3. Criação de Ficha
    path('criando/', criando, name='criando'),
    
    # 4. Galeria e Salvamento (Charsheet) - IMPORTANTE: /charsheet/ (bate com o fetch do JS)
    path('charsheet/', charsheet, name='charsheet'), 

    # 5. Autenticação
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/submit/', user_registration, name='registrar'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    # 6. Recuperação de Senha
    path('password-reset/', password_reset_view, name='password_reset'),
    path('api/password-reset/', password_reset_request, name='api_password_reset'),
    path('password-reset/api/password_recover/', password_recover, name='password_recover'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm_page, name='password_reset_confirm_page'),
    path('password-reset-confirm/', password_reset_confirm, name='password_reset_confirm_api'),
    
    # 7. APIs JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 8. Mesas de Jogo
    path('mesas/', lista_mesas, name='mesas'),
    path('mesas/<int:mesa_id>/', detalhe_mesa, name='detalhe_mesa'),
    path('mesas/<int:mesa_id>/<str:action>/<int:target_id>/', mesa_actions, name='mesa_actions'),
    
    # 9. Feedback
    path('feedback/', feedback, name='feedback'),
]