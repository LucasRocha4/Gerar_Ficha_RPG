a = '''from app_gen_file_rpg.utils import complements, backgrounds, subraces
import random
import requests
import logging

class FillFile():
    def __init__(self, request):
        self.api_base = 'https://www.dnd5eapi.co/api'
        self.data     =  request.POST.dict()
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


    def race_n_class(self):
        self.race_data = {}

        try:
            resp = requests.get(f'{self.api_base}/races/{self.race}')
            resp.raise_for_status()
            self.race_data = resp.json()
            self.speed = self.race_data.get('speed') / 3,281
        finally:
            pass

        self.subrace_data = {}
        if self.subraca:
            try:
                resp = requests.get(f'{self.api_base}/subraces/{self.subraca}')
                resp.raise_for_status()
                self.subrace_data = resp.json()
            except Exception:
                self.subrace_data = subraces.get(self.subraca, {})

        self.class_data = {}
        try:
            resp = requests.get(f'{self.api_base}/classes/{self.classe}')
            resp.raise_for_status()
            self.self.class_data = resp.json()
        finally:
            pass

        self.race_n_class = {
            'race':      self.race_data,
            'class':     self.class_data,
            'subrace':   self.subrace_data,
            'speed':     self.speed
        }
    def atributes(self):

        #atributos base + mod
        atribute = {k: sum(sorted([random.randint(1, 6) for _ in range(4)])[1:]) for k in complements.ATTR_KEYS}
        mod = {complements.ABBRS: complements.MOD_TABLE.get(attr[key, 0]) for complements.ABBRS, key in zip(complements.ABBRS, complements.ATTR_KEYS)}

        #proficiencia do background
        background = self.background
        self.background_skills = [
        prof['name'] for prof in backgrounds.background.get('skill_proficiencies', [])
        ]

        #atributo final
        self.bonus_total = {}
        for b in self.race_data.get('ability_bonuses', []):
            idx = b['ability_score']['index'][:3].lower()
            self.bonus_total[idx] = self.bonus_total.get(idx, 0) + b['bonus']
        for b in self.subrace_data.get('ability_bonuses', []):
            idx = b['ability_score']['index'][:3].lower()
            self.bonus_total[idx] = self.bonus_total.get(idx, 0) + b['bonus']
        print(f'bonus total debug: {self.self.bonus_total}')        

        for attr in complements.ATTR_KEYS:
            abbr = attr[:3]
            if abbr in self.bonus_total:
                original = atribute[attr]
                atribute[attr] += self.bonus_total[abbr]

        salving_throw = [
            {'abbr': s['index'].upper(), 'mod': f"{mod.get(s['index'],0):+d}"}
        for s in self.class_data.get('saving_throws', [])
        ]
        saving_throw_proficiencies = [s['index'].lower() for s in self.class_data.get('saving_throws', [])]

        skills_list = [
            {'name': sk, 'mod': f"{mod.get(ab.lower(),0):+d}"}
            for sk, ab in complements.SKILLS_MAP.items()
        ]

        form_skills = [
            skill['name']
            for skill in skills_list
            if self.data.get(f"{skill['name']}-prof")
        ]

        skill_block = next(
            (c for c in self.class_data.get('proficiency_choices', [])
            if any('Skill: ' in opt['item']['name'] for opt in c.get('from', {}).get('options', []))),
            None
        )

        if skill_block:
            how_many = skill_block['choose']
            skill_choices = [
                opt['item']['name'].replace('Skill: ', '')
                for opt in skill_block['from']['options']
                if 'Skill: ' in opt['item']['name']
            ]
        else:
            how_many = 0
            skill_choices = []

        available_for_class = [
            sk for sk in skill_choices
            if sk not in self.background_skills
            and sk not in form_skills
        ]

        if how_many <= len(available_for_class):
            class_skill_proficiencies = random.sample(available_for_class, k=how_many)
        else:
            class_skill_proficiencies = available_for_class.copy()

        skill_proficiencies = list(set(
            self.background_skills
            + form_skills
            + class_skill_proficiencies
        ))
'''