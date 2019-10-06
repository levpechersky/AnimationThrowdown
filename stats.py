from game import *


def stat_count_by_series(owned_instances):
	count_by_series = {}
	for series in Series:
		count_by_series[series] = 0
	for r_cards in owned_instances.values():
		for instances in r_cards.values():
			for inst in instances:
				count_by_series[inst.series] += 1
	print()
	print("Cards count by series:")
	for series in Series:
		print(" {:16}: {}".format(series, count_by_series[series]))


def stat_count_by_skill(owned_instances, sort=True):
	count_by_skill = {}
	for skill in SKILL_NAME.keys():
		count_by_skill[skill] = 0
	for r_cards in owned_instances.values():
		for instances in r_cards.values():
			for inst in instances:
				for skill in inst.skills.keys():
					count_by_skill[skill] += 1
	print()
	print("Cards count by skill:")
	if sort:
		count_by_skill = sorted(count_by_skill.items(), key=lambda t: t[1], reverse=True)
	for skill, count in count_by_skill:
		print(" {:16}: {}".format(SKILL_NAME[skill], count))


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
		print("\t", c.pretty())
		if limit and i >= limit:
			break

