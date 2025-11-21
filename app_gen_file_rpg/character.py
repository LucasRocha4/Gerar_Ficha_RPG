from    django.http                          import JsonResponse
from    django.conf                          import settings

import os
import  json

def base(request):

    data_file = os.path.join(settings.BASE_DIR, 'static', 'data', 'data.json')

    with open(data_file, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    nome = request.GET.get('nome')
    nivel = request.GET.get('nivel')
    race = request.GET.get('race')
    subrace = request.GET.get('subrace')
    classe = request.GET.get('classe')
    subclasse = request.GET.get('subclasse')
    background = request.GET.get('background')

    personagem = {
        "nome": nome,
        "nivel": nivel,
        "raca": dados["races"].get(race),
        "subraca": dados["subraces"].get(race, {}).get(subrace),
        "classe": dados["classes"].get(classe),
        "subclasse": dados["subclasses"].get(classe, {}).get(subclasse),
        "background": dados["backgrounds"].get(background)
    }


class character():
    def __init__():
        pass