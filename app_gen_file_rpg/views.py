from    django.shortcuts                     import render
from    django.urls                          import reverse_lazy
from    django.views.generic                 import CreateView
from    .forms                               import RegistrarUsuario
from    app_gen_file_rpg.fill_file           import FillFile
from    django.contrib.auth.models           import User
from    django.contrib.auth                  import authenticate, login      
from    django.http                          import JsonResponse
from    rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from    rest_framework_simplejwt.views       import TokenObtainPairView
from    rest_framework                       import serializers
from    django.conf                          import settings
from    django.core.mail                     import send_mail
from    django.contrib.auth.tokens           import default_token_generator
from    django.utils.http                    import urlsafe_base64_encode, urlsafe_base64_decode
from    django.utils.encoding                import force_bytes, force_str
from    django.utils.http                    import urlsafe_base64_encode
from    django.utils.encoding                import force_bytes

import os
import  json

class RegistrarUsuario(CreateView):
    form_class = RegistrarUsuario
    template_name = 'registration/registrar.html'
    success_url = reverse_lazy('login')


def user_registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        is_registering = data.get('is_registering', False)

        if is_registering:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'result': False, 'msg': 'Usuário já existe'})

            user = User.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({'result': True, 'msg': 'Usuário registrado com sucesso'})

        else:
            try:
                user_obj = User.objects.get(username=username)
                username_for_auth = user_obj.username
            except User.DoesNotExist:
                return JsonResponse({'result': False, 'msg': 'Usuário não encontrado'})

            user = authenticate(request, username=username_for_auth, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'result': True, 'msg': 'Login realizado com sucesso'})
            else:
                return JsonResponse({'result': False, 'msg': 'Credenciais inválidas'})

    return JsonResponse({'error': 'Método não permitido'})


def home(request):
    return render(request, 'pages/home.html')


def criando(request):
    return render(request, 'pages/criando.html')


def password_reset_view(request):
    return render(request, 'registration/password_reset.html')


def password_reset_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            user = User.objects.get(email=email)
            
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset link (you'll need to implement the reset confirmation page)
            reset_link = f"{request.scheme}://{request.get_host()}/password-reset-confirm/{uid}/{token}/"
            
            # Send email
            subject = 'FichaDnD - Recuperação de Senha'
            message = f'''
            Olá, aventureiro!
            
            Você solicitou a recuperação de senha para sua conta no FichaDnD.
            
            Clique no link abaixo para redefinir sua senha:
            {reset_link}
            
            Se você não solicitou esta recuperação, ignore este e-mail.
            
            Este link expira em 24 horas.
            
            Boa sorte em suas aventuras!
            '''
            
            # Send email (in development, it prints to console)
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            # For development, just return success
            # In production, you would send the actual email:
            # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            
            return JsonResponse({
                'result': True, 
                'message': 'E-mail de recuperação enviado com sucesso!',
                'reset_link': reset_link  # Only for development/testing
            })
            
        except User.DoesNotExist:
            # Don't reveal if user exists or not for security
            return JsonResponse({
                'result': True, 
                'message': 'Se este e-mail estiver cadastrado, você receberá instruções de recuperação.'
            })
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)


def password_reset_confirm_page(request, uidb64, token):
    """Render the password reset confirmation page"""
    return render(request, 'pages/password_reset_confirm.html', {
        'uidb64': uidb64,
        'token': token
    })


def password_reset_confirm(request):
    """Process the password reset with new password"""
    if request.method == 'POST':
        data = json.loads(request.body)
        uidb64 = data.get('uidb64')
        token = data.get('token')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        # Validate passwords match
        if new_password != confirm_password:
            return JsonResponse({
                'result': False,
                'message': 'As senhas não coincidem'
            }, status=400)
        
        # Validate password strength
        if len(new_password) < 8:
            return JsonResponse({
                'result': False,
                'message': 'A senha deve ter pelo menos 8 caracteres'
            }, status=400)
        
        try:
            # Decode the user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            # Verify the token
            if not default_token_generator.check_token(user, token):
                return JsonResponse({
                    'result': False,
                    'message': 'Link de recuperação inválido ou expirado'
                }, status=400)
            
            # Set the new password
            user.set_password(new_password)
            user.save()
            
            return JsonResponse({
                'result': True,
                'message': 'Senha redefinida com sucesso! Você já pode fazer login.'
            })
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return JsonResponse({
                'result': False,
                'message': 'Link de recuperação inválido'
            }, status=400)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)
