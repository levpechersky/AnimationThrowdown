import os
import xml.etree.ElementTree as ET
from utils import *
from game import *
from collections import defaultdict


def parse_xml(xml_dir, owned_cards=None):
    by_rarity1, by_id1 = parse_cards(os.path.join(xml_dir, "cards.xml"), owned_cards)
    by_rarity2, by_id2 = parse_cards(os.path.join(xml_dir, "cards_mythic.xml"), owned_cards)
    by_rarity3, by_id3 = parse_cards(os.path.join(xml_dir, "cards_finalform.xml"), owned_cards, final_form=True)

    by_rarity = {}
    by_rarity.update(by_rarity1)
    by_rarity.update(by_rarity2)
    by_rarity.update(by_rarity3)

    by_id = {}
    by_id.update(by_id1)
    by_id.update(by_id2)
    by_id.update(by_id3)

    combos = parse_combos(os.path.join(xml_dir, "combos.xml"), by_id)

    return by_rarity, by_id, combos


def parse_cards(path, owned_cards, final_form=False):
    CARDS_BY_RARITY = {}
    for rarity in range(len(RARITY)):
        CARDS_BY_RARITY[rarity] = defaultdict(list)

    CARDS_BY_ID = {}

    xml = ET.parse(path)
    root = xml.getroot()
    for unit in root.findall('unit'):
        c = Card()

        # Internal, not playable cards
        if unit.find('commander') is not None:
            continue

        # Common fields
        c.id = unit.find('id').text
        c.name = unit.find('name').text
        c.rarity = int(unit.find('rarity').text)

        # Optional fields
        if unit.find('trait') is not None:
            c.trait = unit.find('trait').text

        for skill in unit.findall('skill'):
            c.skills.append(_parse_skill(skill))

        if owned_cards and c.name not in owned_cards[c.rarity]:
            continue

        # Type-specific:
        if unit.find('character') is not None:
            c.type = Type.HERO
        elif final_form:
            c.type = Type.POWER
        else:
            c.type = Type.OBJECT

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
