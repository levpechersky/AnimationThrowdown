from game import *
from collections import defaultdict


def stat_entry(string):
	print("\n>> {}".format(string))


def stat_count_by_series(owned_instances):
	stat_entry("Cards count by series:")
	count_by_series = defaultdict(lambda: 0)
	cards_by_series = defaultdict(list)
	for r_cards in owned_instances.values():
		for instances in r_cards.values():
			for inst in instances:
				count_by_series[inst.series] += 1
				cards_by_series[inst.series].append(inst)
	count_by_series = sorted(count_by_series.items(), key=lambda t: t[1], reverse=True)
	for series, count in count_by_series:
		print(" {:16}: {}".format(str(series), count))
	print("Detailed:")
	for series, cards in cards_by_series.items():
		print("	{}".format(series))
		for card in cards:
			print("		{}".format(card.pretty()))


def stat_count_by_skill(owned_instances):
	stat_entry("Cards count by skill:")
	count_by_skill = defaultdict(lambda: 0)
	for r_cards in owned_instances.values():
		for instances in r_cards.values():
			for inst in instances:
				for skill in inst.skills.keys():
					count_by_skill[skill] += 1
	count_by_skill = sorted(count_by_skill.items(), key=lambda t: t[1], reverse=True)
	for skill, count in count_by_skill:
		print(" {:16}: {}".format(SKILL_NAME[skill], count))


def stat_count_by_trait(owned_instances):
	stat_entry("Cards count by trait:")
	count_by_trait = defaultdict(lambda: 0)
	cards_by_trait = defaultdict(list)
	for r_cards in owned_instances.values():
		for instances in r_cards.values():
			for inst in instances:
				if inst.trait:
					count_by_trait[inst.trait] += 1
					cards_by_trait[inst.trait].append(inst)
				else:
					count_by_trait["none"] += 1
	count_by_trait = sorted(count_by_trait.items(), key=lambda t: t[1], reverse=True)
	for trait, count in count_by_trait:
		print(" {:16}: {}".format(trait, count))
	print("Detailed:")
	for trait, cards in cards_by_trait.items():
		print("	{}".format(trait))
		for card in cards:
			print("		{}".format(card.pretty()))


def stat_cards_by_score(owned_instances, limit=None):
	if limit:
		stat_entry("Top {} the most powerful cards:".format(limit))
	else:
		stat_entry("All cards, sorted by power")
	all_cards = []
	for r_cards in owned_instances.values():
		for instances in r_cards.values():
			for inst in instances:
				all_cards.append(inst)
	for i, c in enumerate(sorted(all_cards, key=lambda card: card.score, reverse=True)):
		print("\t", c.pretty())
		if limit and i >= limit:
			break


def strongest_combos_per_card(combo_scores, combo_recipes):
	stat_entry("Strongest combos per card:")
	card_combos = defaultdict(list)
	for combo, score in sorted(combo_scores.items(), key=lambda t: t[1], reverse=True):
		src1, src2 = combo_recipes[combo]
		card_combos[src1].append((src2, combo))
		card_combos[src2].append((src1, combo))
	for inst, combos in card_combos.items():
		print("{}:".format(inst.dump()))
		for other, combo in combos:
			print("	{:7} with {:40}: {}".format(combo.get_score(), other.dump(), combo.pretty()))


def strongest_combos_per_skill(combo_scores, combo_recipes):
	stat_entry("Strongest combos for each skill:")
	# skill -> (combo, [sources...])
	skill_combos = defaultdict(list)
	for combo, score in sorted(combo_scores.items(), key=lambda t: t[1], reverse=True):
		src1, src2 = combo_recipes[combo]
		for skill in combo.skills:
			skill_combos[skill].append((combo, src1, src2))
	for skill, combos in skill_combos.items():
		print("	[{}]".format(SKILL_NAME[skill]))
		combos = sorted(combos, key=lambda t: t[0].skills[skill].x, reverse=True)
		for combo, s1, s2 in combos:
			print("		{:100} | {} + {}".format(combo.pretty(), s1.dump(), s2.dump()))


def strongest_combos(combo_scores, combo_recipes):
	stat_entry("Strongest combos:")
	for inst, _ in sorted(combo_scores.items(), key=lambda t: t[1], reverse=True):
		print("{:120} {} + {}".format(inst.pretty(), combo_recipes[inst][0].dump(), combo_recipes[inst][1].dump()))


def stat_combined_score(inst_scores, inst_combo_scores, combined_score):
	stat_entry("Combined score:")
	combined = map(lambda t: (t[0], combined_score(t[1], inst_scores[t[0]])), inst_combo_scores.items())
	for inst, combo_score in sorted(combined, key=lambda t: t[1], reverse=True):
		print("{:7} {}".format(combo_score, inst.pretty()))


def stat_combo_potential_score(inst_combo_scores):
	stat_entry("Combo potential score:")
	for inst, combo_score in sorted(inst_combo_scores.items(), key=lambda t: t[1], reverse=True):
		print("{:7} {}".format(combo_score, inst.pretty()))


def stat_individual_score(inst_scores, inst_combo_scores):
	stat_entry("Individual card score:")
	for inst, score in sorted(inst_scores.items(), key=lambda t: t[1], reverse=True):
		print("{:7} {}".format(inst_combo_scores[inst], inst.pretty()))
