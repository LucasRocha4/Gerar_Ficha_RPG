from app_gen_file_rpg.utils import complements, backgrounds, subraces
# Certifique-se de que este caminho está correto para o seu arquivo de traduções
import random
import requests

class FillFile:
    def __init__(self, request):
        self.api_base = 'https://www.dnd5eapi.co/api'
        self.session = requests.Session()
        self.data_post = request.POST
        
        # Define o idioma (padrão 'pt')
        self.language = self.data_post.get('lang', request.GET.get('lang', 'pt'))

        self.name = self.data_post.get('charname', '')
        self.playername = self.data_post.get('playername', '')
        self.classe = self.data_post.get('classe', '')
        self.subclasse = self.data_post.get('subclasse', '')
        self.classlevel = self.data_post.get('classlevel', '1')
        self.background_slug = self.data_post.get('antecedente', '')
        self.race = self.data_post.get('race', '')
        self.subraca = self.data_post.get('subrace', '')
        self.alignment = self.data_post.get('alignment', 'Neutral')
        
        self.race_data = {}
        self.class_data = {}
        self.subrace_data = {}
        self.background_data = {}
        self.context = {}

    def _translate_term(self, term, dictionary):
        """Método auxiliar para traduzir termos usando os mapas"""
        key = term.strip()
        # Se o termo está no dicionário (ex: 'Longsword'), retorna a tradução para self.language
        if key in dictionary:
            return dictionary[key].get(self.language, key)
        return term

    @staticmethod
    def normalize_slug(text):
        return text.lower().replace(' ', '-').replace('(', '').replace(')', '')

    def pick_starting_equipment_options(self, options_list):
        choices = []
        for option in options_list:
            if 'from' in option and 'options' in option['from']:
                choose_n = option.get('choose', 1)
                avail_opts = option['from']['options']
                if not avail_opts: continue
                
                picks = random.sample(avail_opts, k=min(choose_n, len(avail_opts)))
                for pick in picks:
                    if 'item' in pick:
                        choices.append(f"1× {pick['item']['name']}")
                    elif 'equipment_category' in pick:
                         choices.append(f"1× {pick['equipment_category']['name']} (Random)")
        return choices

    def fetch_api_data(self):
        try:
            resp = self.session.get(f'{self.api_base}/races/{self.race}')
            resp.raise_for_status()
            self.race_data = resp.json()
            speed_val = self.race_data.get('speed', 30)
            self.speed = int(round(speed_val / 3.281, 1))

            if self.subraca:
                try:
                    resp = self.session.get(f'{self.api_base}/subraces/{self.subraca}')
                    if resp.status_code == 200:
                        self.subrace_data = resp.json()
                    else:
                        if hasattr(subraces, 'subraces'):
                             self.subrace_data = subraces.subraces.get(self.subraca, {})
                        else:
                             self.subrace_data = getattr(subraces, 'data', {}) 
                except Exception:
                    if hasattr(subraces, 'subraces'):
                        self.subrace_data = subraces.subraces.get(self.subraca, {})
                    else:
                        self.subrace_data = {}

            resp = self.session.get(f'{self.api_base}/classes/{self.classe}')
            resp.raise_for_status()
            self.class_data = resp.json()

            self.background_data = backgrounds.backgrounds.get(self.background_slug, {})

        except requests.RequestException:
            pass # Print de erro removido

    def calculate_attributes(self):
        atribute_base = {
            k: sum(sorted([random.randint(1, 6) for _ in range(4)])[1:]) 
            for k in complements.ATTR_KEYS
        }

        bonus_total = {}
        for b in self.race_data.get('ability_bonuses', []):
            idx = b['ability_score']['index'][:3].lower()
            bonus_total[idx] = bonus_total.get(idx, 0) + b['bonus']
            
        for b in self.subrace_data.get('ability_bonuses', []):
            idx = b['ability_score']['index'][:3].lower()
            bonus_total[idx] = bonus_total.get(idx, 0) + b['bonus']
            
        self.final_attributes = {}
        for attr in complements.ATTR_KEYS:
            abbr = attr[:3]
            val = atribute_base.get(attr, 10)
            bonus = bonus_total.get(abbr, 0)
            self.final_attributes[attr] = val + bonus

        self.modifiers = {
            attr[:3]: complements.MOD_TABLE.get(self.final_attributes[attr], 0) 
            for attr in complements.ATTR_KEYS
        }

    def process_skills_and_saves(self):
        attr_keys = ['str', 'dex', 'con', 'int', 'wis', 'cha']
        
        class_saves_slugs = [s['index'].lower() for s in self.class_data.get('saving_throws', [])]
        self.saving_throw_proficiencies = class_saves_slugs

        saving_throws = []
        for abbr in attr_keys:
            base_mod = self.modifiers.get(abbr, 0)
            
            is_proficient = False
            for c_save in class_saves_slugs:
                if c_save.startswith(abbr):
                    is_proficient = True
                    break
            
            final_val = base_mod + (self.proficiencia if is_proficient else 0)
            
            saving_throws.append({
                'abbr': abbr.upper(),
                'mod': f"{final_val:+d}",
                'is_prof': is_proficient
            })

        self.background_skills = [
            prof['name'].replace('Skill: ', '') 
            for prof in self.background_data.get('skill_proficiencies', [])
        ]
        
        form_skills = [
            skill_name
            for skill_name, attr in complements.SKILLS_MAP.items()
            if self.data_post.get(f"{skill_name}-prof")
        ]

        skill_block = next(
            (c for c in self.class_data.get('proficiency_choices', [])
             if 'from' in c and any('Skill: ' in opt['item']['name'] for opt in c['from'].get('options', []))),
            None
        )

        self.skill_choices = []
        class_skill_proficiencies = []
        if skill_block:
            how_many = skill_block.get('choose', 0)
            
            possible_skills = [
                opt['item']['name'].replace('Skill: ', '')
                for opt in skill_block['from']['options']
                if 'Skill: ' in opt['item']['name']
            ]
            self.skill_choices = possible_skills
            
            available = [
                s for s in possible_skills 
                if s not in self.background_skills and s not in form_skills
            ]
            
            if how_many <= len(available):
                class_skill_proficiencies = random.sample(available, k=how_many)
            else:
                class_skill_proficiencies = available

        self.final_skills = list(set(self.background_skills + form_skills + class_skill_proficiencies))
        
        return saving_throws

    def calculate_hp_and_level(self):
        self.hit_die = self.class_data.get('hit_die', 6)
        self.lvl = int(self.classlevel) if self.classlevel.isdigit() else 1
        
        self.hp = self.hit_die + self.modifiers.get('con', 0)
        for _ in range(1, self.lvl):
            self.hp += random.randint(1, self.hit_die) + self.modifiers.get('con', 0)
            
        # Print removido
        self.total_hd = f'{self.lvl}d{self.hit_die}'
        
        self.xp = complements.XP_BY_LEVEL.get(self.lvl, 0)
        idx_prof = min(self.lvl - 1, len(complements.PROFICIENCY_BY_LEVEL) - 1)
        self.proficiencia = complements.PROFICIENCY_BY_LEVEL[idx_prof]

    def process_equipment_and_combat(self):
        background_equipment_list = self.background_data.get("equipment", [])
        
        class_equipment_list = [
            f"{e['quantity']}× {e['equipment']['name']}"
            for e in self.class_data.get('starting_equipment', [])
        ]

        random_choices = self.pick_starting_equipment_options(
            self.class_data.get('starting_equipment_options', [])
        )

        self.all_equipment_list = background_equipment_list + class_equipment_list + random_choices
        
        # --- APLICAÇÃO DE TRADUÇÃO NA LISTA DE EQUIPAMENTOS ---
        translated_equipment = []
        for item in self.all_equipment_list:
            # Separa quantidade do nome (ex: "1× Dagger" ou apenas "Dagger")
            if '×' in item:
                qtd, nome_ingles = item.split('×', 1)
                nome_ingles = nome_ingles.strip()
                nome_traduzido = self._translate_term(nome_ingles, complements.EAPONS_MAP)
                translated_equipment.append(f"{qtd}× {nome_traduzido}")
            else:
                nome_traduzido = self._translate_term(item, complements.WEAPONS_MAP)
                translated_equipment.append(nome_traduzido)

        self.formatted_all_equipment = "\n".join(f"- {item}" for item in translated_equipment)
        # -----------------------------------------------------

        self.armas_mods = {}
        self.armas_dano = {}
        self.nomes_armas = []
        self.best_armor_ca = None
        self.tem_armadura = False

        for item in self.all_equipment_list:
            nome_limpo = item.split('×')[-1].strip()
            
            try:
                resp = self.session.get(f"{self.api_base}/equipment/{self.normalize_slug(nome_limpo)}")
                if resp.status_code != 200: continue
                item_data = resp.json()
                
                cat_idx = item_data.get('equipment_category', {}).get('index')

                if cat_idx == 'weapon':
                    props = [p['index'] for p in item_data.get('properties', [])]
                    cat_range = item_data.get('weapon_range', '')
                    
                    if 'finesse' in props:
                        atributo_usado = 'dex' if self.modifiers['dex'] >= self.modifiers['str'] else 'str'
                    elif cat_range == 'ranged':
                        atributo_usado = 'dex'
                    else:
                        atributo_usado = 'str'

                    base_mod = self.modifiers[atributo_usado]
                    profs_classe = [p['name'].lower() for p in self.class_data.get('proficiencies', [])]
                    
                    tem_prof = any(
                        termo in profs_classe
                        for termo in [
                            item_data.get('name', '').lower(),
                            f"{item_data.get('weapon_category', '')} weapons".lower(),
                            f"{cat_range} weapons".lower(),
                            "simple weapons", "martial weapons"
                        ]
                    )
                    
                    prof_bonus = self.proficiencia if tem_prof else 0
                    mod_final = base_mod + prof_bonus
                    
                    dano = ""
                    dmg_info = item_data.get('damage')
                    if dmg_info and 'damage_dice' in dmg_info:
                        dano = dmg_info['damage_dice']

                    self.nomes_armas.append(nome_limpo)
                    self.armas_mods[nome_limpo] = mod_final
                    self.armas_dano[nome_limpo] = dano

                elif cat_idx == 'armor':
                    self.tem_armadura = True
                    armor_class = item_data.get("armor_class", {})
                    base = armor_class.get("base", 10)
                    dex_bonus = armor_class.get("dex_bonus", False)
                    max_bonus = armor_class.get("max_bonus", None)
                    
                    mod_dex = self.modifiers.get('dex', 0)
                    
                    if not dex_bonus:
                        total_ca = base
                    elif max_bonus is not None:
                        total_ca = base + min(mod_dex, max_bonus)
                    else:
                        total_ca = base + mod_dex
                        
                    if self.best_armor_ca is None or total_ca > self.best_armor_ca:
                        self.best_armor_ca = total_ca
                        
            except requests.RequestException:
                continue

        ca_base = 10 + self.modifiers.get('dex', 0)
        
        if self.tem_armadura and self.best_armor_ca is not None:
            self.ca_final = self.best_armor_ca
        elif self.classe.lower() == "barbarian":
            self.ca_final = 10 + self.modifiers.get('dex', 0) + self.modifiers.get('con', 0)
        elif self.classe.lower() == "monk":
            self.ca_final = 10 + self.modifiers.get('dex', 0) + self.modifiers.get('wis', 0)
        else:
            self.ca_final = ca_base

    def generate_fluff(self):
        outras_proficiencias_background = [
            prof.get('name') for prof in self.background_data.get('tool_proficiencies', [])
        ]

        race_languages = [lang['name'] for lang in self.race_data.get('languages', [])]

        lang_opts = self.background_data.get('language_options') or {}
        choose_val = lang_opts.get('choose', 0)
        how_many = choose_val if isinstance(choose_val, int) else 0

        choice_background_languages = []
        if 0 < how_many <= len(complements.LANGUAGES):
            choice_background_languages = random.sample(complements.LANGUAGES, k=how_many)

        lista_idiomas_ingles = race_languages + choice_background_languages + outras_proficiencias_background
        
        # --- APLICAÇÃO DE TRADUÇÃO NOS IDIOMAS ---
        lista_idiomas_traduzida = [
            self._translate_term(lang, complements.LANGUAGES_MAP) 
            for lang in lista_idiomas_ingles
        ]
        
        self.idiomas = "\n".join(f"- {idioma}" for idioma in lista_idiomas_traduzida)
        # ----------------------------------------

        def pick_trait(key):
            opts = self.background_data.get(key, {}).get('options')
            return random.choice(opts) if opts else None

        self.personality_traits = pick_trait('personality_traits')
        self.ideals = pick_trait('ideals')
        self.bonds = pick_trait('bonds')
        self.flaws = pick_trait('flaws')

    def generate(self):
        self.fetch_api_data()
        self.calculate_attributes()
        self.calculate_hp_and_level()
        
        saves = self.process_skills_and_saves()
        self.process_equipment_and_combat()
        self.generate_fluff()

        race_full = self.race_data.get('name', self.race) + (f" ({self.subraca})" if self.subraca else '')
        classe_full = f"{self.classe} ({self.subclasse}) {self.classlevel}".strip()

        self.context = {
            'charname': self.name,
            'playername': self.playername,
            'classe': classe_full,
            'race': race_full,
            'subrace': self.subraca,
            'background': self.background_slug,
            'alinhamento': self.alignment,
            'experience': 0,
            'xp': self.xp,
            'atributo': self.final_attributes,
            'mod': self.modifiers,
            'saves': saves,
            'saving_throw_proficiencies': self.saving_throw_proficiencies,
            'skill_choices': self.skill_choices,
            'random_skill_proficiencies': self.final_skills,
            'hit_dice': "d"+str(self.hit_die),
            'total_hd': self.total_hd,
            'hp': self.hp,
            'proficiencia': self.proficiencia,
            'speed': self.speed,
            'formatted_all_equipment': self.formatted_all_equipment,
            'armas': self.nomes_armas,
            'armas_mod': self.armas_mods,
            'ca': self.ca_final,
            'idiomas': self.idiomas,
            'personality_traits': self.personality_traits,
            'ideals': self.ideals,
            'bonds': self.bonds,
            'flaws': self.flaws,
        }

        # --- APLICAÇÃO DE TRADUÇÃO NOS ATAQUES (Front-End Labels) ---
        for i, nome_ingles in enumerate(self.nomes_armas[:3]):
            mod = self.armas_mods[nome_ingles]
            dmg = self.armas_dano.get(nome_ingles, "")
            
            # Traduz o nome da arma para exibição
            nome_exibicao = self._translate_term(nome_ingles, complements.WEAPONS_MAP)
            
            self.context[f"atkname{i+1}"]   = nome_exibicao
            self.context[f"atkbonus{i+1}"]  = f"{'+' if mod>=0 else ''}{mod}"
            self.context[f"atkdamage{i+1}"] = dmg
        # ------------------------------------------------------------

        # Print removido
        return self.context