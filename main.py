from collections import defaultdict
from utils import *
from xml_parser import *
from input_parser import *

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
# OWNED_CARDS[rarity][name] -> [Cards...]
OWNED_INSTANCES = {}

# name -> mastery level
MASTERY = {}


def validate_owned(owned_cards, cards_by_rarity):
	missing = []
	for r in range(len(RARITY)):
		for name in owned_cards[r]:
			if cards_by_rarity[r].get(name) is None:
				missing.append((RARITY[r], name))
	if missing:
		raise Exception("Some of your cards not found in game XML: {}. Check Spelling (case-sensitive)".format(missing))


def get_instances(owned_cards):
	new_part("GENERATE CARDS INSTANCES")

	OWNED_INSTANCES = {}
	for r in range(len(RARITY)):
		OWNED_INSTANCES[r] = defaultdict(list)

	for r, cards in owned_cards.items():
		for name, levels in cards.items():
			c = CARDS_BY_RARITY[r][name]
			m = MASTERY.get(name)
			for level in levels:
				OWNED_INSTANCES[r][name].append(c.get_instance(level, m))

	return OWNED_INSTANCES


def statistics(owned_instances):
	new_part("COMPUTING STATISTICS")
	stat_count_by_series(owned_instances)
	stat_cards_by_score(owned_instances, limit=30)


def stat_count_by_series(owned_instances):
	count_by_series = {}
	for series in Series:
		count_by_series[series] = 0
	for r_cards in owned_instances.values():
		for instances in r_cards.values():
			for inst in instances:
				count_by_series[inst.series] += 1
	print()
	print("Cards count:")
	for series in Series:
		print(" {:16}: {}".format(series, count_by_series[series]))


def stat_cards_by_score(owned_instances, limit=None):
	all_cards = []
	for r_cards in owned_instances.values():
		for instances in r_cards.values():
			for inst in instances:
				all_cards.append(inst)
	print()
	if limit:
		print("Top {} the most powerful cards:".format(limit))
	else:
		print("All cards, sorted by power")
	for i, c in enumerate(sorted(all_cards, key=lambda card: card.score, reverse=True)):
		print(c.pretty())
		if limit and i >= limit:
			break


def select_decks():
	new_part("CHOOSING THE BEST DECKS")
	pass  # TODO


def show_decks():
	pass  # TODO


if __name__ == '__main__':
	set_debug(True)

	OWNED_CARDS = read_deck("example.cards")
	debug(" OWNED_CARDS", OWNED_CARDS)

	MASTERY = read_mastery("example.mastery")
	debug(" MASTERY", MASTERY)

	CARDS_BY_RARITY, CARDS_BY_ID, COMBOS = parse_xml(".", OWNED_CARDS)
	validate_owned(OWNED_CARDS, CARDS_BY_RARITY)
	debug(" CARDS_BY_RARITY", CARDS_BY_RARITY)
	debug(" CARDS_BY_ID", CARDS_BY_ID)
	debug(" COMBOS", COMBOS)

	OWNED_INSTANCES = get_instances(OWNED_CARDS)
	debug(" OWNED_INSTANCES", OWNED_INSTANCES)

	statistics(OWNED_INSTANCES)

	select_decks()

	show_decks()
