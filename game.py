import copy
from enum import Enum
from weights import *


class Rarity(Enum):
	NONE = 0
	COMMON = 1
	RARE = 2
	EPIC = 3
	LEGENDARY = 4
	MYTHIC = 5

	def __str__(self):
		return self.name.title()

	def upgrades(self):
		upgrades = [0, 3, 4, 5, 6, 7]
		return upgrades[self.value]

	@staticmethod
	def parse(char):
		format = {"C": 1, "R": 2, "E": 3, "L": 4, "M": 5}
		return Rarity(format[char])


SKILL_NAME = {"give": "Give", "rally": "Cheer", "rallyall": "Cheer All", "inspire": "Motivate", "berserk": "Crazed", "invigorate": "Boost", "outlast": "Recover", "hijack": "Hijack",
	"weaken": "Cripple", "weakenall": "Cripple All", "poison": "Gas", "counter": "Payback", "pierce": "Jab", "strike": "Punch", "shrapnel": "Bomb", "leech": "Leech", "heal": "Heal",
	"healall": "Heal All", "bodyguard": "Bodyguard", "armored": "Sturdy", "barrier": "Shield", "barrierall": "Shield All",
			  "burn": "Burn", "enlarge": "Enlarge"}
# reverse index
SKILL_BY_NAME = {}
for s, n in SKILL_NAME.items():
	SKILL_BY_NAME[n] = s


class Type(Enum):
	NONE = 0
	HERO = 1
	OBJECT = 2
	POWER = 3
	COMBO = 4

	def __str__(self):
		return self.name


class Series(Enum):
	# DO NOT REORDER!
	NONE = 0
	FAMILY_GUY = 1
	AMERICAN_DAD = 2
	BOBS_BURGERS = 3
	KING_OF_THE_HILL = 4
	FUTURAMA = 5

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
		self.y = None  # when skill does not apply for all

	def __str__(self):
		if self.y:
			try:
				y_str = Series(int(self.y))
			except ValueError:
				y_str = self.y
			return "{}({}-{})".format(SKILL_NAME[self.id], self.x, y_str)
		else:
			return "{}({})".format(SKILL_NAME[self.id], self.x)


class Upgrade:
	def __init__(self):
		self.level = 0

		self.attack = 0
		self.hp = 0

		# name -> Skill()
		self.skills = {}


class CardBase:
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

	@classmethod
	def of(cls, other):
		o = cls()

		o.id = other.id
		o.name = other.name
		o.rarity = other.rarity
		o.trait = other.trait

		o.skills = copy.deepcopy(other.skills)

		o.type = other.type
		o.series = other.series

		o.attack = other.attack
		o.hp = other.hp

		return o

	def _apply_mastery(self, mastery):
		assert isinstance(mastery, int) and mastery > 0

		m = 1 + 0.1 * mastery
		self.attack = int(self.attack * m)
		self.hp = int(self.hp * m)
		for skill in self.skills.values():
			skill.x = int(skill.x * m)

	def _get_score(self):
		a = self.attack * ATTACK_WEIGHT
		h = self.hp * HP_WEIGHT
		s = 0
		for skill in self.skills.values():
			s_name = SKILL_NAME[skill.id]
			w = SKILL_WEIGHTS[s_name]
			if not skill.y:
				s += skill.x * w
			else:
				s += skill.x * 0.5 * w

		return int(a + h + s)

	def __str__(self):
		# skills = [s.id for s in self.skills]
		# return "[{} {} {} {} ({})]".format(self.id, self.name, str(self.type)[5:], RARITY[self.rarity], str(skills)[1:-1])
		return "[{} {} {} {}]".format(self.id, self.name, self.type.name, self.rarity)

	def __repr__(self):
		return str(self)

	def get_series(self):
		id = self.id
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


class CardProto(CardBase):
	# if has <commander> - discard
	def __init__(self):
		super(CardProto, self).__init__()

		# Base card
		self.upgrades = []
		# attack, hp - inherited

		# Combo
		self.m_attack = 0.0
		self.m_hp = 0.0

	def get_instance(self, level, mastery=None):
		if not self.upgrades:
			raise Exception("No levels are defined for the card {} #{}".format(self.name, self.id))

		instance = CardInstance.of(self)
		instance.set_stats(self.upgrades, level, mastery)
		return instance


class CardInstance(CardBase):
	def __init__(self):
		super(CardInstance, self).__init__()

		self.level = 0
		self.score = 0

	def get_score(self):
		if self.level == 0:
			raise Exception("Instance of {} #{} has undefined level".format(self.name, self.id))
		return self.score

	def pretty(self):
		skill_s = [str(s) for s in self.skills.values()]
		return "{:10} {:2}/{:2}[{:5}] {:28} {:6} {:16} {}".format(self.rarity, self.attack, self.hp, self.score, self.name, self.type.name, self.series, ' '.join(skill_s))

	def dump(self):
		fuses, level = divmod(self.level, self.rarity.upgrades())
		level_str = "{}{}".format(level + self.rarity.upgrades(), "*"*(fuses-1))
		return "{} {} {}".format(self.rarity, level_str, self.name)

	def set_stats(self, upgrades, level, mastery=None):
		assert self.type != Type.COMBO
		assert upgrades and level

		self.level = level

		for up in sorted(upgrades, key=lambda u: u.level):
			if up.hp > 0:
				self.hp = up.hp
			if up.attack > 0:
				self.attack = up.attack
			for skill in up.skills.values():
				self.skills[skill.id] = skill
			if up.level >= level:
				break

		if mastery:
			self._apply_mastery(mastery)

		self.score = self._get_score()


class CardCombo(CardBase):
	def __init__(self):
		super(CardCombo, self).__init__()

		self.score = 0

	def set_stats(self, mastery):
		if mastery:
			self._apply_mastery(mastery)

		self.score = self._get_score()

	def get_score(self):
		return self.score

	def pretty(self):
		skill_s = [str(s) for s in self.skills.values()]
		return "{:28} {:2}/{:2}[{:5}] {}".format(self.name, self.attack, self.hp, self.score, ' '.join(skill_s))


def is_power_card(id):
	return 110001 <= id <= 160000
