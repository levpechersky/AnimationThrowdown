
from enum import Enum


RARITY = ["N/A", "Common", "Rare", "Epic", "Legendary", "Mythic"]
RARITY_UPGRADES = [0, 3, 4, 5, 6, 7]
RARITY_FORMAT = {"C": 1, "R": 2, "E": 3, "L": 4, "M": 5}

SKILL_NAME = {
    "give": "Give",
    "rally": "Cheer",
    "rallyall": "Cheer All",
    "inspire": "Motivate",
    "berserk": "Crazed",
    "invigorate": "Boost",
    "outlast": "Recover",
    "hijack": "Hijack",
    "weaken": "Cripple",
    "weakenall": "Cripple All",
    "poison": "Gas",
    "counter": "Payback",
    "pierce": "Jab",
    "strike": "Punch",
    "shrapnel": "Bomb",
    "leech": "Leech",
    "heal": "Heal",
    "healall": "Heal All",
    "bodyguard": "Bodyguard",
    "armored": "Sturdy",
    "barrier": "Shield",
    "barrierall": "Shield All",
}


class Type(Enum):
    NONE = 0
    HERO = 1
    OBJECT = 2
    POWER = 3


class Skill:
    def __init__(self):
        self.id = ""

        # Base card
        self.x = 0

        # Combo
        self.p = 0
        self.v = 0
        self.y = 0  # when skill does not apply for all


class Card:
    # if has <commander> - discard
    def __init__(self):
        self.id = 0
        self.name = ""
        self.rarity = 0
        self.trait = ""

        self.skills = []

        self.type = Type.NONE

        # Base card
        self.attack = 0
        self.hp = 0
        self.upgrades = []

        # Combo
        self.m_attack = 0.0
        self.m_hp = 0.0

    def __str__(self):
        # skills = [s.id for s in self.skills]
        # return "[{} {} {} {} ({})]".format(self.id, self.name, str(self.type)[5:], RARITY[self.rarity], str(skills)[1:-1])
        return "[{} {} {} {}]".format(self.id, self.name, str(self.type)[5:], RARITY[self.rarity])

    def __repr__(self):
        return str(self)

    def get(self, level, mastery=0):
        # TODO
        pass

