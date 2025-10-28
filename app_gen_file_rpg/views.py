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
            if User.objects.filter(email=email).exists():
                return JsonResponse({'result': False, 'msg': 'Usuário já existe'})

            user = User.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({'result': True, 'msg': 'Usuário registrado com sucesso'})

        else:
            try:
                user_obj = User.objects.get(email=email)
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


## JWT LOGIN PERSONALIZADO PARA USAR EMAIL
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user_obj = User.objects.get(email=email)
            username_for_auth = user_obj.username
        except User.DoesNotExist:
            raise Exception("Credenciais inválidas")

        user = authenticate(username=username_for_auth, password=password)
        if user is None:
            raise Exception("Credenciais inválidas")

        # Faz login na sessão
        request = self.context.get('request')
        login(request, user)

        # Gera tokens JWT
        data = super().validate({
            "username": username_for_auth,
            "password": password
        })
        data.update({"msg": "Login realizado com sucesso"})

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception:
            return JsonResponse({
                "result": False,
                "msg": "Credenciais inválidas"
            }, status=401)


def home(request):
    return render(request, 'pages/home.html')


def criando(request):
    return render(request, 'pages/criando.html')