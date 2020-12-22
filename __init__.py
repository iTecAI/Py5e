from common import *
from creature import Creature
import json

'''c = Creature.from_parameters(
    name='Orc',
    alignment='lawful neutral',
    creature_type={'type':'humanoid','tags':['orc']},
    proficiency_bonus=2,
    speeds={'walk':30},
    max_hp=15,
    armor_class=13,
    scores={
        'strength':[16,False,0],
        'dexterity':[12,False,0],
        'constitution':[16,False,0],
        'intelligence':[7,False,0],
        'wisdom':[11,False,0],
        'charisma':[10,False,0]
    },
    skills={
        'intimidation':[True,False,0]
    },
    senses={'darkvision':60}
)

print(json.dumps(c.to_dict(),indent=4))

c2 = Creature(c.to_dict())
print(json.dumps(c2.to_dict(),indent=4))'''