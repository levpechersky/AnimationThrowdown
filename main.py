from collections import defaultdict
from utils import *
from stats import *
from game_db import *
from player_cards import *

# Google doc with stats
# https://docs.google.com/spreadsheets/d/14wUFB7iVjP8ETCvgcBsGm_i5HgU7ecYFo1ivRoVPGlw/edit#gid=924965638

# http://cb-live.synapse-games.com/assets/combo_recipe.xml
# http://cb-live.synapse-games.com/assets/combo.xml

def validate_owned(owned_cards, cards_by_rarity):
	missing = []
	for r in Rarity:
		for name in owned_cards[r]:
			if cards_by_rarity[r].get(name) is None:
				missing.append((r, name))
	if missing:
		raise Exception("Some of your cards not found in game XML: {}. Check Spelling (case-sensitive)".format(missing))


def instantiate_all_cards(player_cards, game_db):
	new_part("GENERATE CARDS INSTANCES")

	owned_instances = {}
	for r in Rarity:
		owned_instances[r] = defaultdict(list)

	for pcard in player_cards:
		inst = game_db.instantiate(pcard.rarity, pcard.name, pcard.level)
		owned_instances[pcard.rarity][pcard.name].append(inst)

	return owned_instances


def instantiate_all_combos(player_cards, game_db, heros, objects):
	new_part("GENERATE ALL POSSIBLE COMBOS")

	# combo_instances[inst 1][inst 2] -> Combo
	combo_instances = defaultdict(dict)

	for hero in heros:
		for obj in objects:
			combo_proto = game_db.combo_of(hero.id, obj.id)
			if combo_proto is None:
				continue

			mastery = player_cards.mastery_level(combo_proto.name)

			instance = CardCombo.of(combo_proto)

			instance.attack = int(1.1 * (hero.attack + obj.attack) * combo_proto.m_attack)
			instance.hp = int(1.1 * (hero.hp + obj.hp) * combo_proto.m_hp)

			combo_power = 1.1 * (3 * (hero.attack + obj.attack) + hero.hp + obj.hp)
			for skill in instance.skills.values():
				skill.x = int((combo_power - skill.p) * (skill.v - 1) / (100 - skill.p) + 1)

			instance.set_stats(mastery)

			combo_instances[hero][obj] = instance

	n_combos = sum([len(x) for x in combo_instances.values()])
	print("Successfully instantiated {} combos from {} hero and {} object cards"
		  .format(n_combos, len(heros), len(objects)))
	return combo_instances


def split_instances(instances):
	heros = []
	objects = []

	# OWNED_INSTANCES[pcard.rarity][pcard.name].append(inst)
	for r_cards in instances.values():
		for c_instances in r_cards.values():
			for inst in c_instances:
				assert isinstance(inst, CardInstance)
				if inst.type == Type.HERO:
					heros.append(inst)
				if inst.type == Type.OBJECT:
					objects.append(inst)

	return heros, objects


def compute_scores(instances, combo_instances):
	# combo instance -> score
	combo_scores = {}

	# instance -> [combos...]
	instance_combos = defaultdict(list)

	for hero, h_combos in combo_instances.items():
		for obj, combo in h_combos.items():
			combo_scores[combo] = combo.get_score()
			instance_combos[hero].append(combo)
			instance_combos[obj].append(combo)

	# card instance -> sum of all it's combos score
	instance_combo_scores = defaultdict(lambda: 0)

	for inst, combos in instance_combos.items():
		for combo in combos:
			instance_combo_scores[inst] += combo_scores[combo]

	# instance -> score
	instance_scores = {}

	# owned_instances[pcard.rarity][pcard.name].append(inst)
	for r_cards in instances.values():
		for c_list in r_cards.values():
			for inst in c_list:
				instance_scores[inst] = inst.get_score()

	return instance_scores, instance_combo_scores, combo_scores


def combined_score(combos_score, instance_score):
	return ((combos_score // 15) * COMBOS_SCORE_WEIGHT + instance_score * SINGLE_CARD_SCORE_WEIGHT) // (COMBOS_SCORE_WEIGHT + SINGLE_CARD_SCORE_WEIGHT)


def statistics(owned_instances):
	new_part("COMPUTING STATISTICS")
	stat_count_by_series(owned_instances)
	stat_count_by_skill(owned_instances)
	stat_cards_by_score(owned_instances)


def select_decks():
	new_part("CHOOSING THE BEST DECKS")
	pass  # TODO


def show_decks():
	pass  # TODO


if __name__ == '__main__':
	set_debug(False)

	cards_xmls = ["cards.xml", "cards_finalform.xml", "cards_mythic.xml"]
	combos_xml = "combos.xml"
	char_combos_xml = "combo_recipe.xml"
	game_db = GameDB(cards_xmls, combos_xml, char_combos_xml)
	game_db.load()

	deck = "deck.cards"
	side = "sidedeck.cards"
	mastery = "example.mastery"
	player_cards = PlayerCards(deck, side, mastery)
	player_cards.load()

	instances = instantiate_all_cards(player_cards, game_db)
	heros, objects = split_instances(instances)
	combo_instances = instantiate_all_combos(player_cards, game_db, heros, objects)

	inst_scores, inst_combo_scores, combo_scores = compute_scores(instances, combo_instances)
	print("Individual card score:")
	for inst, score in sorted(inst_scores.items(), key=lambda t: t[1], reverse=True):
		print("{:7} {}".format(inst_combo_scores[inst], inst.pretty()))

	print("Combo potential score:")
	for inst, combo_score in sorted(inst_combo_scores.items(), key=lambda t: t[1], reverse=True):
		print("{:7} {}".format(combo_score, inst.pretty()))

	print("Combined score:")
	combined = map(lambda t: (t[0], combined_score(t[1], inst_scores[t[0]])), inst_combo_scores.items())
	for inst, combo_score in sorted(combined, key=lambda t: t[1], reverse=True):
		print("{:7} {}".format(combo_score, inst.pretty()))

	print("Strongest combos:")
	for inst, score in sorted(combo_scores.items(), key=lambda t: t[1], reverse=True):
		print("{:7} {}".format(score, inst.pretty()))

	# statistics(instances)

	select_decks()

	show_decks()
