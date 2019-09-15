from collections import defaultdict
from utils import *
from xml_parser import *
from input_parser import *


# Reddit thread about combo stats
# https://www.reddit.com/r/AnimationThrowdown/comments/5l69n2/do_you_have_any_ideas_how_the_combo_stats_are/

# Google doc with stats
# https://docs.google.com/spreadsheets/d/14wUFB7iVjP8ETCvgcBsGm_i5HgU7ecYFo1ivRoVPGlw/edit#gid=924965638


# id -> Card
CARDS_BY_ID = {}

# CARDS_BY_RARITY[rarity][name] -> Card
CARDS_BY_RARITY = {}

# COMBOS[id1][id2] -> Card
COMBOS = {}

# OWNED_CARDS[rarity][name] -> [levels...]
OWNED_CARDS = {}

# name -> mastery level
MASTERY = {}


def select_decks():
    pass  # TODO


def show_decks():
    pass  # TODO


if __name__ == '__main__':
    set_debug(True)

    # TODO argparse

    print()
    print("READING DECK")
    OWNED_CARDS = read_deck("example.cards")
    debug(" OWNED_CARDS", OWNED_CARDS)

    print()
    print("READING COMBO MASTERY STATS")
    MASTERY = read_mastery("example.mastery")
    debug(" MASTERY", MASTERY)

    print()
    print("PARSING GAME CARDS XML")
    CARDS_BY_RARITY, CARDS_BY_ID, COMBOS = parse_xml(".", OWNED_CARDS)
    debug(" CARDS_BY_RARITY", CARDS_BY_RARITY)
    debug(" CARDS_BY_ID", CARDS_BY_ID)
    debug(" COMBOS", COMBOS)

    print()
    print("CHOOSING THE BEST DECKS")
    select_decks()

    print()
    print("READY")
    show_decks()
