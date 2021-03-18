from requests.api import get
from .common import *
from .creature import Creature
from .character import Character
from .npc import NPC

# Utility functions
import requests

def url(endpoint):
    return f'https://critterdb.com/api/{endpoint}'

def get_published_bestiary_creatures(id):
    raws = []
    current = [0]
    p = 1
    while len(current) > 0:
        current = requests.get(url(f'publishedbestiaries/{id}/creatures/{str(p)}')).json()
        raws.extend(current)
        p += 1
    
    name = requests.get(url(f'publishedbestiaries/{id}')).json()['name']

    return name, [NPC.from_pycritter(i) for i in raws]

def get_bestiary_creatures(id):
    name = requests.get(url(f'bestiaries/{id}')).json()['name']
    return name, [NPC.from_pycritter(i) for i in requests.get(url(f'bestiaries/{id}/creatures/')).json()]

def get_critterdb_creature(id):
    return NPC.from_pycritter(requests.get(url(f'creatures/{id}')).json())
