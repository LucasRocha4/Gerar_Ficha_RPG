from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import RegistrarUsuario
from app_gen_file_rpg.fill_file import FillFile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login      
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from app_gen_file_rpg.utils.complements import get_labels, translate_saves_list
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import FichaPersonagem, Mesa, ParticipacaoMesa

import json
import ast

def sanitize_data(data):
    if isinstance(data, str):
        return data.strip()
    elif isinstance(data, dict):
        return {k: sanitize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(v) for v in data]
    else:
        return data


@login_required 
def charsheet(request):
    if request.method == 'POST':
        try:
            raw_body = request.body.decode('utf-8')
            if not raw_body:
                return JsonResponse({'error': 'Nenhum dado recebido.'}, status=400)

            data = json.loads(raw_body)

            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    try:
                        data = ast.literal_eval(data)
                    except:
                        return JsonResponse({'error': 'Formato de dados inválido.'}, status=400)

            if not isinstance(data, dict):
                 return JsonResponse({'error': 'Dados inválidos (Esperado um objeto JSON).'}, status=400)

            clean_data = sanitize_data(data)
            
            nome = clean_data.get('charname', 'Sem Nome')
            classe_full = str(clean_data.get('classe', 'Desconhecido'))
            
            try:
                nivel = int(clean_data.get('classlevel', 1))
            except (ValueError, TypeError):
                nivel = 1

            ficha, created = FichaPersonagem.objects.update_or_create(
                usuario=request.user,
                nome_personagem=nome,
                defaults={
                    'classe': classe_full,
                    'nivel': nivel,
                    'dados_ficha': clean_data
                }
            )

            msg = "Ficha criada com sucesso!" if created else "Ficha atualizada com sucesso!"
            return JsonResponse({'message': msg, 'id': ficha.id}, status=200)

        except Exception as e:
            print(f"ERRO NO SERVIDOR: {e}")
            return JsonResponse({'error': f"Erro interno: {str(e)}"}, status=500)
    
    else:
        fichas = FichaPersonagem.objects.filter(usuario=request.user).order_by('-data_atualizacao')
        return render(request, 'pages/charsheet.html', {'fichas': fichas})


def criando(request):
    target_lang = request.GET.get('lang', request.POST.get('lang', 'pt'))
    
    load_id = request.GET.get('load_id')
    if load_id and request.user.is_authenticated:
        try:
            ficha = FichaPersonagem.objects.get(id=load_id, usuario=request.user)
            request.session['ficha_data'] = ficha.dados_ficha
            return redirect('criando')
        except FichaPersonagem.DoesNotExist:
            pass 

    context = {}

    if request.method == 'POST':
        try:
            gerador = FillFile(request)
            data_context = gerador.generate()
            request.session['ficha_data'] = data_context
            context = data_context.copy()
        except Exception as e:
            print(f"Erro na geração: {e}")
            return render(request, 'pages/erro.html', {'erro': 'Erro na geração'})

    elif request.method == 'GET':
        data_context = request.session.get('ficha_data')
        if not data_context:
            return redirect('home')
        context = data_context.copy()

    context['full_data_json'] = request.session.get('ficha_data', context)

    context['labels'] = get_labels(target_lang)
    
    if 'saves' in context:
        context['saves'] = translate_saves_list(context['saves'], target_lang)

    context['current_lang'] = target_lang
    request.session['ultima_ficha'] = context
    
    return render(request, 'pages/criando.html', context)



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
            login(request, user)
            return JsonResponse({'result': True, 'msg': 'Usuário registrado e logado!'})
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                return JsonResponse({'result': True, 'msg': 'Login realizado'})
            else:
                return JsonResponse({'result': False, 'msg': 'Credenciais inválidas'})
    return JsonResponse({'error': 'Método não permitido'})

def home(request):
    context = {'user': request.user}
    return render(request, 'pages/home.html', context)

def password_reset_view(request): return render(request, 'registration/password_reset.html')

@csrf_exempt
def password_reset_request(request):

    return JsonResponse({'msg': 'ok'}) 

def password_recover(request): return render(request, 'pages/password_recover.html')
def password_reset_confirm_page(request, uidb64, token): return render(request, 'pages/password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
def password_reset_confirm(request): return JsonResponse({'msg': 'ok'})

@login_required
def lista_mesas(request):
    if request.method == 'POST':
        nome = request.POST.get('nome_mesa')
        desc = request.POST.get('descricao')
        if nome:
            Mesa.objects.create(mestre=request.user, nome=nome, descricao=desc)
            return redirect('mesas')

    minhas_mesas = Mesa.objects.filter(mestre=request.user)
    mesas_participando = Mesa.objects.filter(participantes__jogador=request.user)

    return render(request, 'pages/mesas_list.html', {
        'minhas_mesas': minhas_mesas,
        'mesas_participando': mesas_participando
    })

@login_required
def detalhe_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    is_mestre = (mesa.mestre == request.user)
    
    participacao = ParticipacaoMesa.objects.filter(mesa=mesa, jogador=request.user).first()
    
    if not is_mestre and not participacao:
        participacao = ParticipacaoMesa.objects.create(mesa=mesa, jogador=request.user)
    
    if request.method == 'POST' and 'vincular_ficha' in request.POST:
        ficha_id = request.POST.get('ficha_id')
        if ficha_id and participacao:
            ficha = get_object_or_404(FichaPersonagem, id=ficha_id, usuario=request.user)
            participacao.ficha = ficha
            participacao.save()
            return redirect('detalhe_mesa', mesa_id=mesa.id)

    participantes = Mesa.objects.get(id=mesa_id).participantes.all().select_related('jogador', 'ficha')
    
    minhas_fichas = FichaPersonagem.objects.filter(usuario=request.user)

    return render(request, 'pages/mesa_detail.html', {
        'mesa': mesa,
        'is_mestre': is_mestre,
        'participantes': participantes,
        'minhas_fichas': minhas_fichas,
        'participacao_atual': participacao,
        'absolute_uri': request.build_absolute_uri() 
    })

@login_required
def mesa_actions(request, mesa_id, action, target_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    if mesa.mestre != request.user:
        return redirect('detalhe_mesa', mesa_id=mesa.id)
    
    target_user = get_object_or_404(User, id=target_id)

    if action == 'kick':
        ParticipacaoMesa.objects.filter(mesa=mesa, jogador=target_user).delete()
    
    elif action == 'promote':

        if not ParticipacaoMesa.objects.filter(mesa=mesa, jogador=request.user).exists():
            ParticipacaoMesa.objects.create(mesa=mesa, jogador=request.user)
            
        mesa.mestre = target_user
        mesa.save()
        
    return redirect('detalhe_mesa', mesa_id=mesa.id)
