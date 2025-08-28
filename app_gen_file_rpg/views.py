from    django.shortcuts            import render
from    django.urls                 import reverse_lazy
from    django.views.generic        import CreateView
from    .forms                      import RegistrarUsuario
from    app_gen_file_rpg.fill_file  import FillFile
from    django.contrib.auth.models  import User
from    django.contrib.auth         import authenticate, login      
from    django.http                 import JsonResponse
import  json

class RegistrarUsuario(CreateView):
    form_class      = RegistrarUsuario
    template_name   = 'registration/registrar.html'
    success_url     = reverse_lazy('login')

def user_registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        username = data.get('username')
        email    = data.get('email')
        password = data.get('password')

        is_registering = data.get('is_registering', False)

        if is_registering:
            if User.objects.filter(email = email).exists():
                return JsonResponse({'result' : False, 'msg': 'user alredy exist'})
            
            user = User.objects.create_user(username = username, password = password, email = email)
            user.save()
            return JsonResponse({'result': True, 'msg': 'user registred'})
        
        else:
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return JsonResponse({'result': True, 'msg': 'login sucessfully'})
            else:
                return JsonResponse({'result': False, 'msg': 'login invalid'})
        
    return JsonResponse({'error': 'method no allowed'})
    
def home(request):
    return render(request, 'pages/home.html')

def criando(request):
    return render(request, 'pages/criando.html')

