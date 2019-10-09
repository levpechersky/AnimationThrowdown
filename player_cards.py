import re
from game import *
from utils import *
from collections import defaultdict


class PlayerCard:
	def __init__(self, rarity, name, level, in_deck):
		self.rarity = rarity
		self.name = name
		self.level = level
		self.in_deck = in_deck

	def __str__(self):
		return "{:10} {:30} level {:2}".format(self.rarity, self.name, self.level)


class PlayerCards:
	CARD_RE = re.compile(r'([CRELM])\s+(\d\**)\s+(\S+.*\S+)')
	MASTERY_RE = re.compile(r'(\d\**)\s+(\S+.*\S+)')

	def __init__(self, deck, side, mastery):
		self.deck_path = deck
		self.side_deck_path = side
		self.mastery_path = mastery

		# self.cards[rarity][name] -> [PlayerCard...]
		self.cards = {}
		for rarity in Rarity:
			self.cards[rarity] = defaultdict(list)

		self.mastery = {}

	def load(self):
		new_part("READING DECK")
		self._read_deck(self.deck_path, in_deck=True)
		if self.side_deck_path:
			self._read_deck(self.side_deck_path, in_deck=False)

		n_cards = sum([len(r_cards) for r_cards in self.cards.values()])
		print("Successfully loaded {} cards (not including duplicates)".format(n_cards))

		new_part("READING COMBO MASTERY STATS")
		self._read_mastery()

		print("Successfully loaded {} mastered combos".format(len(self.mastery)))

	def _read_deck(self, path, in_deck):

		with open(path) as f:
			for line in f:
				# discard whitespace, empty or comment lines
				if line.isspace() or line.startswith("#"):
					continue

				m = self.CARD_RE.match(line)
				if m is None:
					raise Exception("Failed to parse card '{}'".format(line))

				rarity_text = m.group(1)
				level_text = m.group(2)
				name = m.group(3)

				rarity = Rarity.parse(rarity_text)

				# Legendary 4** -> n_fuses=2, level=(2*6 + 4)=16
				# Epic 5        -> n_fuses=0, level=(0*5 + 5)=5
				n_fuses = len(level_text) - 1
				i_level = int(level_text[0])
				if i_level > rarity.upgrades():
					raise Exception("Level {} is too high for an {} card".format(i_level, rarity))
				level = n_fuses * rarity.upgrades() + i_level

				pc = PlayerCard(rarity, name, level, in_deck)
				self.cards[rarity][name].append(pc)
				debug(pc)

	def _read_mastery(self):
		with open(self.mastery_path) as f:
			for line in f:
				# discard whitespace, empty or comment lines
				if line.isspace() or line.startswith("#"):
					continue

				m = self.MASTERY_RE.match(line)
				if m is None:
					raise Exception("Failed to parse mastery '{}'".format(line))

				mastery_level = int(m.group(1))
				name = m.group(2)
				debug("mastery_level='{}' name='{}'".format(mastery_level, name))

				self.mastery[name] = mastery_level

	def __iter__(self):
		for r_cards in self.cards.values():
			for instances in r_cards.values():
				for pcard in instances:
					yield pcard

	# return None if no mastery
	def mastery_level(self, combo_name):
		return self.mastery.get(combo_name)
