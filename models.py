from pydantic import BaseModel

from typing import List


class Card(BaseModel):
    name: str
    region: str
    cost: int
    descriptionRaw: str
    keywords: List[str]
    rarity: str
    type: str
    cardCode: str
    associatedCardRefs: List[str]


class Ability(Card):
    pass


class Trap(Card):
    # Currently only Teemo's Poison Puffcap
    pass


class Unit(Card):
    attack: int
    health: int
    levelupDescriptionRaw: str
    subtype: str


class Spell(Card):
    spellSpeed: str
