#!/usr/bin/env python3

import argparse
import datetime
import sys
from stats import *
from game_db import *
from player_cards import *


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
	# Combo -> (inst1, inst2)
	combo_recipes = {}

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
			combo_recipes[instance] = (hero, obj)

	n_combos = sum([len(x) for x in combo_instances.values()])
	print("Successfully instantiated {} combos from {} hero and {} object cards".format(n_combos, len(heros), len(objects)))
	return combo_instances, combo_recipes


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


def statistics(owned_instances, inst_scores, inst_combo_scores, combo_scores, combo_recipes):
	new_part("COMPUTING STATISTICS")
	stat_count_by_series(owned_instances)
	stat_count_by_skill(owned_instances)
	stat_count_by_trait(owned_instances)
	# stat_cards_by_score(owned_instances)
	stat_individual_score(inst_scores, inst_combo_scores)
	stat_combo_potential_score(inst_combo_scores)
	stat_combined_score(inst_scores, inst_combo_scores, combined_score)
	strongest_combos(combo_scores, combo_recipes)
	strongest_combos_per_card(combo_scores, combo_recipes)
	strongest_combos_per_skill(combo_scores, combo_recipes)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--deck_only", action='store_true', help="Only process cards in the active deck")
	parser.add_argument("-o", "--output", default='report.txt', type=argparse.FileType('w'), help="Write output to file")
	parser.add_argument("-D", "--debug", action='store_true', help="Print additional debug info")
	args = parser.parse_args()

	if args.debug:
		set_debug(True)

	if args.output:
		sys.stdout = args.output

	# Read Game Cards Data
	cards_xmls = ["cards.xml", "cards_finalform.xml", "cards_mythic.xml"]
	combos_xml = "combos.xml"
	char_combos_xml = "combo_recipe.xml"
	game_db = GameDB(cards_xmls, combos_xml, char_combos_xml)
	game_db.load()

	# Read Player Cards Data
	deck = "deck.cards"
	side = "sidedeck.cards"
	if args.deck_only:
		side = None
	mastery = "combo.mastery"
	player_cards = PlayerCards(deck, side, mastery)
	player_cards.load()

	# Instantiate Cards and Combos
	instances = instantiate_all_cards(player_cards, game_db)
	heros, objects = split_instances(instances)
	combo_instances, combo_recipes = instantiate_all_combos(player_cards, game_db, heros, objects)
	inst_scores, inst_combo_scores, combo_scores = compute_scores(instances, combo_instances)

	# Report
	statistics(instances, inst_scores, inst_combo_scores, combo_scores, combo_recipes)

	print("Report generated on {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
