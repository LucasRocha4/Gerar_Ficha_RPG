from app_gen_file_rpg.utils import complements, backgrounds, subraces
import requests
import logging

class FillFile():
    def __init__(self):
        self.api_base = 'https://www.dnd5eapi.co/api'
        pass
    def data(request, self):
        self.data       = request.POST.dict()
        self.name       = self.data.get('charname', '')
        self.classe     = self.data.get('classe', '')
        self.subclasse  = self.data.get('subclasse', '')
        self.classlevel = self.data.get('classlevel', '')
        self.background = self.data.get('antecedente', '')
        self.race       = self.data.get('race', '')
        self.subraca    = self.data.get('subrace', '')


    def raca_e_classe(self):
        race_data = {}

        try:
            resp = requests.get(f'{self.api_base}/races/{self.race}')
            resp.raise_for_status()
            race_data = resp.json()
            speed = race_data.get('speed')
        finally:
            pass

        subrace_data = {}
        if self.subraca:
            try:
                resp = requests.get(f'{self.api_base}/subraces/{self.subraca}')
                resp.raise_for_status()
                subrace_data = resp.json()
            except Exception:
                subrace_data = subraces.get(self.subraca, {})

        class_data = {}
        try:
            resp = requests.get(f'{self.api_base}/classes/{self.classe}')
            resp.raise_for_status()
            class_data = resp.json()
        finally:
            pass        
    def atributes(self):

        #atributos base + mod
        attr = {k: complements.gen_atributos for k in complements.ATTR_KEYS}
        mod = {complements.ABBRS: complements.MOD_TABLE.get(attr[key, 0]) for complements.ABBRS, key in zip(complements.ABBRS, complements.ATTR_KEYS)}

        #proficiencia do background
        background = self.background
        background_skills = [
        prof['name'] for prof in backgrounds.background.get('skill_proficiencies', [])
        ]
        

