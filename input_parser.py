import re
from game import *
from utils import *
from collections import defaultdict


CARD_RE = re.compile(r'([CRELM])\s+(\d\**)\s+(\S+.*\S+)')
MASTERY_RE = re.compile(r'(\d\**)\s+(\S+.*\S+)')


def read_deck(deck_path):
    OWNED_CARDS = {}
    for rarity in range(len(RARITY)):
        OWNED_CARDS[rarity] = defaultdict(list)

    with open(deck_path) as f:
        for line in f:
            # discard whitespace, empty or comment lines
            if line.isspace() or line.startswith("#"):
                continue

            m = CARD_RE.match(line)
            if m is None:
                raise Exception("Failed to parse card '{}'".format(line))

            rarity_text = m.group(1)
            level_text = m.group(2)
            name = m.group(3)

            rarity = RARITY_FORMAT[rarity_text]

            # Legendary 4** -> n_fuses=2, level=(2*6 + 4)=16
            # Epic 5        -> n_fuses=0, level=(0*5 + 5)=5
            n_fuses = len(level_text) - 1
            i_level = int(level_text[0])
            if i_level > RARITY_UPGRADES[rarity]:
                raise Exception("Level {} is too high for an {} card".format(level, RARITY[rarity]))
            level = n_fuses * RARITY_UPGRADES[rarity] + i_level

            OWNED_CARDS[rarity][name].append(level)

            debug("{:10} {:30} level {:2}".format(RARITY[rarity], name, level))

    return OWNED_CARDS


def read_mastery(mastery_path):
    MASTERY = {}

    with open(mastery_path) as f:
        for line in f:
            # discard whitespace, empty or comment lines
            if line.isspace() or line.startswith("#"):
                continue

            m = MASTERY_RE.match(line)
            if m is None:
                raise Exception("Failed to parse mastery '{}'".format(line))

            mastery_level = int(m.group(1))
            name = m.group(2)
            debug("mastery_level='{}' name='{}'".format(mastery_level, name))

            MASTERY[name] = mastery_level

    return MASTERY