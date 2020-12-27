from common import *
from creature import *
import os

class Character(Creature):
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
        race,
        level,
        background,
        hit_dice,
        equipped,
        proficiencies,
        attacks,
        spellcasting,
        appearance,
        inventory,
        traits,
        source=None
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
        dct['race'] = race
        dct['level'] = level
        dct['background'] = background
        dct['hit_dice'] = hit_dice
        dct['equipped'] = equipped
        dct['proficiencies'] = proficiencies
        dct['attacks'] = attacks
        dct['spellcasting'] = spellcasting
        dct['appearance'] = appearance
        dct['inventory'] = inventory
        dct['traits'] = traits
        dct['source'] = source

        return cls(dct)
    
    def __init__(self, dct):
        super().__init__(dct)
        self.race = dct['race']
        self.level = dct['level']
        self.background = dct['background']
        self.hit_dice = dct['hit_dice']
        self.equipped = dct['equipped']
        self.proficiencies = dct['proficiencies']
        self.attacks = dct['attacks']
        self.spellcasting = dct['spellcasting']
        self.appearance = dct['appearance']
        self.inventory = dct['inventory']
        self.traits = dct['traits']
        self.source = dct['source']
    
    @classmethod
    def from_gsheet(cls,sheet_id,api_path):
        source = {
            'type':'google_sheet',
            'sheet_id':sheet_id
        }

        engine = get_gapi(api_path)

        ranges = {
            'v2.1!c6':'name',
            'v2.1!c15':'abStr',
            'v2.1!c20':'abDex',
            'v2.1!c25':'abCon',
            'v2.1!c30':'abInt',
            'v2.1!c35':'abWis',
            'v2.1!c40':'abCha',
            'v2.1!h17:h22':'saveProfs',
            'v2.1!u16':'hp',
            'v2.1!r12':'ac',
            'v2.1!h25:h42':'skillProfs',
            'v2.1!r25':'hitDice',
            'v2.1!h14':'proficiency',
            'v2.1!t7':'race',
            'v2.1!t5':'classes',
            'v2.1!ae7':'xp',
            'v2.1!al6':'level',
            'v2.1!aj11':'background',
            'v2.1!ae12:ae14':'personalityTraits',
            'v2.1!ae16:ae18':'ideals',
            'v2.1!ae20:ae22':'bonds',
            'v2.1!ae24:ae26':'flaws',
            'v2.1!aj28':'alignment',
            'v2.1!i49':'armorProfs',
            'v2.1!i50':'weaponProfs',
            'v2.1!i51':'vehicleProfs',
            'v2.1!i52':'toolProfs',
            'v2.1!i53':'otherProfs',
            'v2.1!i54':'otherSpeeds',
            'v2.1!z12':'speed',
            'v2.1!r45:r56':'languages',
            'v2.1!ac45:ac56':'equippedItems',
            'v2.1!c59:n84':'traits0',
            'v2.1!p59:aa84':'traits1',
            'v2.1!ac59:an84':'traits2',
            'additional!t69:t79':'resistances',
            'additional!ab69:ab79':'immunities',
            'additional!ai69:ai79':'vulnerabilities',
            'v2.1!n96:n98':'spell0-0',
            'v2.1!x96:x98':'spell0-1',
            'v2.1!ah96:ah98':'spell0-2',
            'v2.1!d100:d104':'spell1-0',
            'v2.1!n100:n104':'spell1-1',
            'v2.1!x100:x104':'spell1-2',
            'v2.1!n106:n110':'spell2-0',
            'v2.1!x106:x110':'spell2-1',
            'v2.1!ah106:ah110':'spell2-2',
            'v2.1!d112:d116':'spell3-0',
            'v2.1!n112:n116':'spell3-1',
            'v2.1!x112:x116':'spell3-2',
            'v2.1!n118:n122':'spell4-0',
            'v2.1!x118:x122':'spell4-1',
            'v2.1!ah118:ah122':'spell4-2',
            'v2.1!d123:d126':'spell5-0',
            'v2.1!n123:n126':'spell5-1',
            'v2.1!x123:x126':'spell5-2',
            'v2.1!n128:n131':'spell6-0',
            'v2.1!x128:x131':'spell6-1',
            'v2.1!ah128:ah131':'spell6-2',
            'v2.1!d133:d135':'spell7-0',
            'v2.1!n133:n135':'spell7-1',
            'v2.1!x133:x135':'spell7-2',
            'v2.1!n137:n139':'spell8-0',
            'v2.1!x137:x139':'spell8-1',
            'v2.1!ah137:ah139':'spell8-2',
            'v2.1!d141:d143':'spell9-0',
            'v2.1!n141:n143':'spell9-1',
            'v2.1!x141:x143':'spell9-2',
            'v2.1!c148':'age',
            'v2.1!f148':'height',
            'v2.1!i148':'weight',
            'v2.1!l148':'size',
            'v2.1!c150':'gender',
            'v2.1!f150':'eyes',
            'v2.1!i150':'hair',
            'v2.1!l150':'skin',
            'v2.1!c176':'appearance',
            'v2.1!r147:r162':'alliesOrganizations',
            'v2.1!i176':'symbolUrl',
            'v2.1!r165:r177':'backstory',
            'inventory!d3':'coinCp',
            'inventory!d6':'coinSp',
            'inventory!d9':'coinEp',
            'inventory!d12':'coinGp',
            'inventory!d15':'coinPp',
            "'attack info'!b7:ao201":'attackInfo',
            "'gear info'!b7:ao201":'gearInfo',
            "'race info'!b7:ao201":'raceInfo',
            "'class info'!b7:ao201":'classInfo'
        }
        [ranges.__setitem__('v2.1!p'+str(i+17),ABILITIES[i]+'SaveAdv') for i in range(6)]
        [ranges.__setitem__('v2.1!p'+str(i+25),list(SKILLS.keys())[i]+'SkillAdv') for i in range(17)]
        [ranges.__setitem__('inventory!i'+str(i+3),'inventoryCount'+str(i)) for i in range(74)]
        [ranges.__setitem__('inventory!j'+str(i+3),'inventory'+str(i)) for i in range(74)]
        [ranges.__setitem__('inventory!r'+str(i+3),'inventoryCost'+str(i)) for i in range(74)]
        [ranges.__setitem__('inventory!u'+str(i+3),'inventoryWeight'+str(i)) for i in range(74)]
        [ranges.__setitem__('inventory!z'+str(i+3),'inventoryCount'+str(i+74)) for i in range(74)]
        [ranges.__setitem__('inventory!aa'+str(i+3),'inventory'+str(i+74)) for i in range(74)]
        [ranges.__setitem__('inventory!ai'+str(i+3),'inventoryCost'+str(i+74)) for i in range(74)]
        [ranges.__setitem__('inventory!al'+str(i+3),'inventoryWeight'+str(i+74)) for i in range(74)]

        vals = engine.spreadsheets().values().batchGet(spreadsheetId=sheet_id,ranges=list(ranges.keys()),valueRenderOption='UNFORMATTED_VALUE').execute().get('valueRanges',[])
        [i.__setitem__('values',[]) for i in vals if not 'values' in i.keys()]
        preloaded = {ranges[x['range'].lower()]:x['values'] for x in vals}
        for k in preloaded.keys():
            for i in range(2):
                if len(preloaded[k]) == 1:
                    preloaded[k] = preloaded[k][0]
            if type(preloaded[k]) == list:
                for i in range(len(preloaded[k])):
                    if type(preloaded[k][i]) == list and len(preloaded[k][i]) == 1:
                        preloaded[k][i] = preloaded[k][i][0]
            if type(preloaded[k]) == str:
                try:
                    preloaded[k] = int(preloaded[k])
                except ValueError:
                    pass
            if preloaded[k] == [] or preloaded[k] == '-':
                preloaded[k] = None
        
        listify = [
            'equippedItems','languages','traits0','traits1','traits2','resistances','immunities','vulnerabilities',
            'spell0-0','spell0-1','spell0-2','spell1-0','spell1-1','spell1-2','spell2-0','spell2-1','spell2-2',
            'spell3-0','spell3-1','spell3-2','spell4-0','spell4-1','spell4-2','spell5-0','spell5-1','spell5-2',
            'spell6-0','spell6-1','spell6-2','spell7-0','spell7-1','spell7-2','spell8-0','spell8-1','spell8-2',
            'spell9-0','spell9-1','spell9-2'
        ]
        for k in listify:
            if type(preloaded[k]) != list:
                preloaded[k] = [preloaded[k]]
            if preloaded[k] == [None]:
                preloaded[k] = []
        for k in ['attackInfo','gearInfo','raceInfo','classInfo']:
            new = []
            for i in preloaded[k]:
                _new = []
                for d in i:
                    if not d == '':
                        _new.append(d)
                if len(_new) > 0:
                    if _new[0] != '':
                        new.append(_new)
            preloaded[k] = new[:]
        
        for s in range(10):
            new = []
            for c in range(3):
                new.extend(preloaded[f'spell{str(s)}-{str(c)}'])
                del preloaded[f'spell{str(s)}-{str(c)}']
            preloaded[f'spell{str(s)}'] = new[:]
        traits = []
        [traits.extend(preloaded['traits'+str(c)]) for c in range(3)]
        del preloaded['traits0']
        del preloaded['traits1']
        del preloaded['traits2']
        preloaded['traits'] = traits[:]

        inventory = []
        for i in range(148):
            if preloaded['inventory'+str(i)] != None:
                inventory.append({
                    'name':preloaded['inventory'+str(i)],
                    'quantity':preloaded['inventoryCount'+str(i)],
                    'cost':preloaded['inventoryCost'+str(i)],
                    'weight':preloaded['inventoryWeight'+str(i)]
                })
            del preloaded['inventory'+str(i)]
            del preloaded['inventoryCount'+str(i)]
            del preloaded['inventoryCost'+str(i)]
            del preloaded['inventoryWeight'+str(i)]
        
        preloaded['inventory'] = inventory[:]

        newInfo = []
        cats = ['name','damage','type','proficiency_category','range_class','monk_weapon','enchant_bonus','bonus_damage','bonus_type','ability_override','properties','apply_mod']
        for item in preloaded['attackInfo']:
            d = {cats[i]:condition(item[i]=='-',None,item[i]) for i in range(len(item))}
            if d['name'] != 0:
                newInfo.append(d)
        preloaded['attackInfo'] = newInfo[:]
        newInfo = []
        cats = ['name','ac_bonus','max_dex','category','required_str','stealth_mod','enchantment_bonus','proficiency_bonus','skills_bonus','saves_bonus','properties']
        for item in preloaded['gearInfo']:
            newInfo.append({cats[i]:condition(item[i]=='-',None,item[i]) for i in range(len(item))})
        preloaded['gearInfo'] = newInfo[:]
        newInfo = []
        cats = ['name','scores','armor','speed','hp_bonus','resist_immune_vuln','languages','attacks','weapon_armor_profs','other_proficiencies']
        for item in preloaded['raceInfo']:
            newInfo.append({cats[i]:condition(item[i]=='-',None,item[i]) for i in range(len(item))})
        preloaded['raceInfo'] = newInfo[:]
        newInfo = []
        cats = ['name','subclass','alt_ac','hit_die','init_bonus','bonus_hp','saves_skills','first_level_profs','multiclass_profs','spell_type','spell_ability','speed_increase']
        for item in preloaded['classInfo']:
            newInfo.append({cats[i]:condition(item[i]=='-',None,item[i]) for i in range(len(item))})
        preloaded['classInfo'] = newInfo[:]

        with open('preload.json','w') as f:
            f.write(json.dumps(preloaded,indent=4))


Character.from_gsheet('1Yd91902ynVYzd_wzR0mVck_ejaxwK5FTSa-EbyFtfBc',os.path.join('local','gapi.json'))
