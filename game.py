import copy
from enum import Enum

RARITY = ["N/A", "Common", "Rare", "Epic", "Legendary", "Mythic"]
RARITY_UPGRADES = [0, 3, 4, 5, 6, 7]
RARITY_FORMAT = {"C": 1, "R": 2, "E": 3, "L": 4, "M": 5}

SKILL_NAME = {
	"give": "Give",
	"rally": "Cheer",
	"rallyall": "Cheer All",
	"inspire": "Motivate",
	"berserk": "Crazed",
	"invigorate": "Boost",
	"outlast": "Recover",
	"hijack": "Hijack",
	"weaken": "Cripple",
	"weakenall": "Cripple All",
	"poison": "Gas",
	"counter": "Payback",
	"pierce": "Jab",
	"strike": "Punch",
	"shrapnel": "Bomb",
	"leech": "Leech",
	"heal": "Heal",
	"healall": "Heal All",
	"bodyguard": "Bodyguard",
	"armored": "Sturdy",
	"barrier": "Shield",
	"barrierall": "Shield All",
}
# reverse index
SKILL_BY_NAME = {}
for s, n in SKILL_NAME.items():
	SKILL_BY_NAME[n] = s


class Type(Enum):
	NONE = 0
	HERO = 1
	OBJECT = 2
	POWER = 3


class Series(Enum):
	NONE = 0
	FAMILY_GUY = 1
	AMERICAN_DAD = 2
	FUTURAMA = 3
	BOBS_BURGERS = 4
	KING_OF_THE_HILL = 5

	def __str__(self):
		return self.name.replace("_", " ").title()


class Skill:
	def __init__(self):
		self.id = ""

		# Base card
		self.x = 0

		# Combo
		self.p = 0
		self.v = 0
		self.y = 0  # when skill does not apply for all


class Upgrade:
	def __init__(self):
		self.level = 0

		self.attack = 0
		self.hp = 0

		# name -> Skill()
		self.skills = {}


class Card:
	# if has <commander> - discard
	def __init__(self):
		self.id = 0
		self.name = ""
		self.rarity = 0
		self.trait = ""

		# name -> Skill()
		self.skills = {}

		self.type = Type.NONE
		self.series = Series.NONE

		self.attack = 0
		self.hp = 0

		# instance only:
		self.level = 0

	def __str__(self):
		# skills = [s.id for s in self.skills]
		# return "[{} {} {} {} ({})]".format(self.id, self.name, str(self.type)[5:], RARITY[self.rarity], str(skills)[1:-1])
		return "[{} {} {} {}]".format(self.id, self.name, self.type.name, RARITY[self.rarity])

	def __repr__(self):
		return str(self)

	def get_series(self):
		id = self.id
		# 	Family Guy Input   10001 - 14000
		# 	Family Guy Combo   15001 - 20000
		#
		# 	American Dad Input 20001 - 24000
		# 	American Dad Combo 25001 - 30000
		#
		# 	Bob's Burgers Input 30001 - 34000
		# 	Bob's Burgers Combo 35001 - 40000
		#
		# 	King of the Hill Input 40001 - 44000
		# 	King of the Hill Combo 45001 - 50000
		#
		# 	Futurama Input 50001 - 54000
		# 	Futurama Combo 55001 - 60000
		if id == 0:
			raise Exception("Card id unknown")

		if 10001 <= id <= 14000 or 15001 <= id <= 20000 or 110001 <= id <= 120000:
			return Series.FAMILY_GUY

		if 20001 <= id <= 24000 or 25001 <= id <= 30000 or 120001 <= id <= 130000:
			return Series.AMERICAN_DAD

		if 30001 <= id <= 34000 or 35001 <= id <= 40000 or 130001 <= id <= 140000:
			return Series.BOBS_BURGERS

		if 40001 <= id <= 44000 or 45001 <= id <= 50000 or 140001 <= id <= 150000:
			return Series.KING_OF_THE_HILL

		if 50001 <= id <= 54000 or 55001 <= id <= 60000 or 150001 <= id <= 160000:
			return Series.FUTURAMA


	def get_score(self):
		pass # TODO


class CardProto(Card):
	# if has <commander> - discard
	def __init__(self):
		super(CardProto, self).__init__()

		# Base card
		self.upgrades = []
		# attack, hp - inherited

		# Combo
		self.m_attack = 0.0
		self.m_hp = 0.0

	def get_instance(self, level, mastery=0):
		if not self.upgrades:
			raise Exception("No levels are defined for the card {} #{}".format(self.name, self.id))

		instance = copy.copy(self)

		instance.level = level

		for up in sorted(self.upgrades, key=lambda u: u.level):
			if up.hp > 0:
				instance.hp = up.hp
			if up.attack > 0:
				instance.attack = up.attack
			for skill in up.skills.values():
				instance.skills[skill.id] = skill
			if up.level >= level:
				break

		if mastery > 0:
			m = 1 + 0.1 * mastery
			instance.attack = int(instance.attack * m)
			instance.hp = int(instance.hp * m)
			for skill in instance.skills:
				skill.x = int(skill.x * m)

		return instance


def get_combo(card1, card2, combos, cards_by_id):
	combo_card_id = combos[card1.id][card2.id]
	combo_card = cards_by_id[combo_card_id]

	instance = copy.deepcopy(combo_card)

	instance.attack = int(1.1 * (card1.attack + card2.attack) * combo_card.m_attack)
	instance.hp = int(1.1 * (card1.hp + card2.hp) * combo_card.m_hp)

	# A combo power is calculated using formula:
	# 1.1 × (3 × (character.attack + item.attack) + character.health + item.health)
	# Then, given parameters p and v for each skill (from the XML files),
	# each skill value is calculated using formula:
	# floor( (combo power - p) × (v - 1) ÷ (100 - p) + 1 )

	combo_power = 1.1 * (3 * (card1.attack + card2.attack) + card1.hp + card2.hp)
	for skill in combo_card.skills:
		skill.x = int((combo_power - skill.p) * (skill.v - 1) / (100 - skill.p) + 1)

	return instance
