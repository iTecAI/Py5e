from common import *
from creature import *

import requests

open5e_url = 'https://api.open5e.com/monsters/'

class NPC(Creature):
    @classmethod
    def from_parameters(
        cls, 
        name, 
        alignment,
        size,
        creature_type, 
        proficiency_bonus, 
        speeds, 
        max_hp, 
        armor_class, 
        scores, 
        skills, 
        senses, 
        immunities, 
        resistances, 
        vulnerabilities, 
        condition_immunities,
        languages,
        challenge_rating,
        traits,
        actions,
        legendary_actions,
        reactions
    ):
        dct = cls.creature_from_parameters(
            name=name, 
            alignment=alignment,
            size=size, 
            creature_type=creature_type, 
            proficiency_bonus=proficiency_bonus, 
            speeds=speeds, 
            max_hp=max_hp, 
            armor_class=armor_class, 
            scores=scores, 
            skills=skills, 
            senses=senses, 
            immunities=immunities, 
            resistances=resistances, 
            vulnerabilities=vulnerabilities, 
            condition_immunities=condition_immunities,
            languages=languages
        )
        dct['challenge_rating'] = challenge_rating
        dct['traits'] = traits
        dct['actions'] = actions
        dct['legendary_actions'] = legendary_actions
        dct['reactions'] = reactions
        return cls(dct)
    
    def __init__(self, dct):
        super().__init__(dct)
        self.challenge_rating = dct['challenge_rating']
        self.traits = dct['traits']
        self.actions = dct['actions']
        self.legendary_actions = dct['legendary_actions']
        self.reactions = dct['reactions']
    
    @classmethod
    def from_open5e(cls,dict5e,roll_hp=False):
        if eval(dict5e['challenge_rating']) > 20:
            proficiency = int((eval(dict5e['challenge_rating'])/5)+3)
        else:
            proficiency = int((eval(dict5e['challenge_rating'])/5)+2)

        scores = {}
        for ability in ABILITIES:
            scores[ability] = [
                dict5e[ability],
                dict5e[f'{ability}_save'] != None,
                False
            ]
            if dict5e[f'{ability}_save'] != None:
                scores[ability].append(dict5e[f'{ability}_save'])
        
        skills = {}
        for skill in dict5e['skills'].keys():
            if skill in SKILLS.keys():
                skills[skill] = [True,False,0,dict5e['skills'][skill]]
        
        senses = {s.split(' ')[0]:int(s.split(' ')[1]) for s in dict5e['senses'].split(', ') if not s.startswith('passive')}

        immunities = []
        for segment in dict5e['damage_immunities'].split('; '):
            for damage in DAMAGETYPES:
                if damage in segment.split(', '):
                    item = {'type':damage,'flags':[]}
                    for flag in DAMAGEFLAGS:
                        if flag in segment:
                            if f"aren't {flag}" in segment:
                                item['flags'].append('!'+flag)
                            else:
                                item['flags'].append(flag)
                    immunities.append(item)
        resistances = []
        for segment in dict5e['damage_resistances'].split('; '):
            for damage in DAMAGETYPES:
                if damage in segment.split(', '):
                    item = {'type':damage,'flags':[]}
                    for flag in DAMAGEFLAGS:
                        if flag in segment:
                            if f"aren't {flag}" in segment:
                                item['flags'].append('!'+flag)
                            else:
                                item['flags'].append(flag)
                    resistances.append(item)
        vulnerabilities = []
        for segment in dict5e['damage_vulnerabilities'].split('; '):
            for damage in DAMAGETYPES:
                if damage in segment.split(', '):
                    item = {'type':damage,'flags':[]}
                    for flag in DAMAGEFLAGS:
                        if flag in segment:
                            if f"aren't {flag}" in segment:
                                item['flags'].append('!'+flag)
                            else:
                                item['flags'].append(flag)
                    vulnerabilities.append(item)
        
        actions = []
        if dict5e['actions'] != '':
            for i in dict5e['actions']:
                actions.append(Action.from_open5e_damage(i))

        return cls.from_parameters(
            dict5e['name'],
            dict5e['alignment'],
            dict5e['size'],
            {
                'type':dict5e['type'],
                'tags':condition(len(dict5e['subtype'])>0,dict5e['subtype'].split(', '),[])
            },
            proficiency,
            dict5e['speed'],
            condition(roll_hp,d20.roll(dict5e['hit_dice']).total,dict5e['hit_points']),
            dict5e['armor_class'],
            scores,
            skills,
            senses,
            immunities,
            resistances,
            vulnerabilities,
            [c for c in dict5e['condition_immunities'] if c in CONDITIONS],
            dict5e['languages'].split(', '),
            eval(dict5e['challenge_rating']),
            condition(dict5e['special_abilities']=='',[],dict5e['special_abilities']),
            actions,
            condition(dict5e['legendary_actions']=='',None,{
                'description':dict5e['legendary_desc'],
                'actions':dict5e['legendary_actions']
            }),
            condition(dict5e['reactions']=='',[],dict5e['reactions'])
        )

npc = NPC.from_open5e(requests.get(open5e_url,params={'search':'adult green dragon'}).json()['results'][0])
npc2 = NPC(npc.to_dict())
print(json.dumps(npc.to_dict(),indent=4))
print(json.dumps(npc2.to_dict(),indent=4))
    