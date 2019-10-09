#!/usr/bin/python3

import random
import sys
from collections import namedtuple
from utils import *

Card = namedtuple("Card", ['attack', 'hp', 'skill', 'skill_value'])


SKILLS = ["HP", "Attack", "Punch", "Bomb", "Crazed", "Gas", "Give", "Cheer", "Cheer All", "Motivate",
			"Heal", "Heal All", "Cripple", "Cripple All", "Bodyguard", "Sturdy", "Shield", "Shield All",
			"Payback", "Boost", "Recover", "Hijack", "Leech", "Jab", "Burn", "Enlarge"]


SKILL_HINTS = {
	"Motivate": "+ attack for neighbors",
	"Bodyguard": "fence",
	"Sturdy": "brick wall",
	"Boost": "+ attack on combo",
	"Recover": "+ hp on combo",
	"Hijack": "steal",
	"Leech": "heal when dealing damage",
	"Jab": "piercing damage",
	"Enlarge": "+ hp for each enemy card",
	"Burn": "damage to enemy with most hp"
}


def get_choice(i_str):
	while True:
		try:
			return int(input(i_str))
		except EOFError:
			sys.exit(0)
		except ValueError:
			print("[ERROR] Please, enter a number")
			continue


def gen_cards(stat1, v1, stat2, v2):
	a = random.randint(5, 20)
	h = random.randint(10, 50)

	a1, h1, a2, h2 = 0, 0, 0, 0

	if stat1 == "HP":
		h1 = v1
	if stat1 == "Attack":
		a1 = v1
	if stat2 == "HP":
		h2 = v2
	if stat2 == "Attack":
		a2 = v2

	c1 = Card(attack=a + a1, hp=h + h1, skill=stat1, skill_value=v1)
	c2 = Card(attack=a + a2, hp=h + h2, skill=stat2, skill_value=v2)

	return c1, c2


# Returns True if user wants to retry
def trade(skill_1, v1, skill_2):
	hint1 = "({})".format(SKILL_HINTS[skill_1]) if SKILL_HINTS.get(skill_1) else ""
	hint2 = "({})".format(SKILL_HINTS[skill_2]) if SKILL_HINTS.get(skill_2) else ""
	trade_str = "For how much {}{} would you trade {}({})?\nEnter 0 to try with new random {} value.\n".format(skill_2, hint2, skill_1, v1, skill_1)

	v2 = 0
	while True:
		v2 = get_choice(trade_str)
		if v2 == 0:
			return True

		c1, c2 = gen_cards(skill_1, v1, skill_2, v2)

		s1_str = "with {}({}) {}".format(c1.skill, c1.skill_value, hint1) if skill_1 not in ["HP", "Attack"] else ""
		s2_str = "with {}({}) {}".format(c2.skill, c2.skill_value, hint2) if skill_2 not in ["HP", "Attack"] else ""
		i_str = "Let's check. Which is stronger?\n 0: both are equal, proceed to next skill\n 1: {:2}/{:2} card {}\n 2: {:2}/{:2} card {}\n".format(c1.attack, c1.hp, s1_str, c2.attack, c2.hp, s2_str)
		c = get_choice(i_str)
		while c not in [0, 1, 2]:
			print("Please enter 0, 1 or 2")
			c = get_choice(i_str)
		if c == 0:
			break
		if c == 1:
			print("Increase value, try {}".format(random.randint(v2, 2 * v2)))
		if c == 2:
			print("Decrease value, try {}".format(random.randint(1, v2)))

	w = int(v1 * W_SKILLS[skill_1] / v2)
	W_SKILLS[skill_2] = w
	print("Set weight {}={}".format(skill_2, w))
	print("=" * 50)

	return False


W_BASE = 100
W_SKILLS = {}
for s in SKILLS:
	W_SKILLS[s] = W_BASE

# All skills in Attack units
random.shuffle(SKILLS)  # to make it less boring
for i, skill in enumerate(SKILLS):
	if skill == "Attack":
		continue

	retry = True
	while retry:
		retry = trade("Attack", random.randint(1, 15), skill)

	if (len(SKILLS) - i) % 5 == 0:
		print("\n*** Good Job! Only {} skills left! ***\n".format(len(SKILLS) - i))

# Show
print("# COMPUTED WEIGHTS")
print("# Paste this into weights.py at the end of file.")
print("HP_WEIGHT = {}\nATTACK_WEIGHT = {}\nSKILL_WEIGHTS = {{".format(W_SKILLS["HP"], W_SKILLS["Attack"]))
for skill, w in sorted(W_SKILLS.items(), key=lambda t: t[1], reverse=True):
	if skill not in ["HP", "Attack"]:
		hint = "  # {}".format(SKILL_HINTS[skill]) if SKILL_HINTS.get(skill) else ""
		print("	'{}': {},{}".format(skill, w, hint))
print("}")
