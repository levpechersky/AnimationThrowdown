import os
import xml.etree.ElementTree as ET
from utils import *
from game import *
from collections import defaultdict


def parse_xml(xml_dir, owned_cards=None):
    by_rarity1, by_id1 = parse_cards(os.path.join(xml_dir, "cards.xml"), owned_cards)
    by_rarity2, by_id2 = parse_cards(os.path.join(xml_dir, "cards_mythic.xml"), owned_cards)
    by_rarity3, by_id3 = parse_cards(os.path.join(xml_dir, "cards_finalform.xml"), owned_cards, final_form=True)

    by_rarity = by_rarity1
    for r in range(len(RARITY)):
        by_rarity[r].update(by_rarity2[r])
        by_rarity[r].update(by_rarity3[r])

    by_id = by_id1
    by_id.update(by_id1)
    by_id.update(by_id2)
    by_id.update(by_id3)

    combos = parse_combos(os.path.join(xml_dir, "combos.xml"), by_id)

    return by_rarity, by_id, combos


def parse_cards(path, owned_cards, final_form=False):
    CARDS_BY_RARITY = {}
    for rarity in range(len(RARITY)):
        CARDS_BY_RARITY[rarity] = {}

    CARDS_BY_ID = {}

    xml = ET.parse(path)
    root = xml.getroot()
    for unit in root.findall('unit'):
        c = CardProto()

        # Internal, not playable cards
        if unit.find('commander') is not None:
            continue

        # Common fields
        c.id = int(unit.find('id').text)
        c.name = unit.find('name').text
        c.rarity = int(unit.find('rarity').text)

        # Optional fields
        if unit.find('trait') is not None:
            c.trait = unit.find('trait').text
        if unit.find('health') is not None:
            c.hp = int(unit.find('health').text)
        if unit.find('attack') is not None:
            c.attack = int(unit.find('attack').text)
        if unit.find('health_multiplier') is not None:
            c.m_hp = float(unit.find('health_multiplier').text)
        if unit.find('attack_multiplier') is not None:
            c.m_attack = float(unit.find('attack_multiplier').text)

        for skill in unit.findall('skill'):
            s = _parse_skill(skill)
            c.skills[s.id] = s

        for upgrade in unit.findall('upgrade'):
            c.upgrades.append(_parse_upgrade(upgrade))

        if owned_cards and c.name not in owned_cards[c.rarity]:
            continue

        # Type-specific:
        if unit.find('character') is not None:
            c.type = Type.HERO
        elif final_form:
            c.type = Type.POWER
        else:
            c.type = Type.OBJECT

        c.series = c.get_series()

        debug(c)
        CARDS_BY_RARITY[c.rarity][c.name] = c

        CARDS_BY_ID[c.id] = c

    return CARDS_BY_RARITY, CARDS_BY_ID


def _parse_skill(skill):
    s = Skill()
    s.id = skill.get('id')
    # some of those may be None
    s.p = skill.get('p')
    s.v = skill.get('v')
    s.x = skill.get('x')
    s.y = skill.get('y')
    return s


def _parse_upgrade(upgrade):
    u = Upgrade()
    u.level = int(upgrade.find('level').text)

    hp = upgrade.find('health')
    if hp is not None:
        u.hp = int(hp.text)

    at = upgrade.find('attack')
    if at is not None:
        u.attack = int(at.text)

    for skill in upgrade.findall('skill'):
        s = _parse_skill(skill)
        u.skills[s.id] = s

    return u


# by_id used as filter
def parse_combos(path, by_id):
    COMBOS = defaultdict(dict)

    xml = ET.parse(path)
    root = xml.getroot()
    for combo in root.findall('combo'):
        cards = combo.find('cards')
        id = combo.find('card_id').text
        c1 = cards.get('card1')
        c2 = cards.get('card2')

        if c1 in by_id and c2 in by_id:
            COMBOS[c1][c2] = id
            COMBOS[c2][c1] = id

    return COMBOS
