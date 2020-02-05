from pydantic import BaseModel

from typing import List


class Card(BaseModel):
    name: str
    region: str
    cost: int
    descriptionRaw: str
    keywords: List[str]
    rarity: str
    subtype: str
    type: str
    cardCode: str
    associatedCardRefs: List[str]

    def get_comment(self): ...


class Unit(Card):
    attack: int
    health: int
    levelupDescriptionRaw: str

    def get_comment(self):
        return f"**Cost**: {self.cost} | **Attack**: {self.attack} | **Health**: {self.health} | " \
               f"**Keywords**: {', '.join(self.keywords)}  \n" \
               f"**Description**: *{self.descriptionRaw or self.levelupDescriptionRaw}*  \n" \
               f"**Level Up**: *{self.levelupDescriptionRaw}*"


class Spell(Card):
    spellSpeed: str

    def get_comment(self):
        return f"**Cost**: {self.cost} | **Speed**: {self.spellSpeed}  \n" \
               f"**Description**: *{self.descriptionRaw}*"


class Ability(Card):

    def get_comment(self):
        return f"**Cost**: {self.cost}  \n" \
               f"**Description**: *{self.descriptionRaw}*"


class Trap(Ability):
    # Currently only Teemo's Poison Puffcap
    pass
