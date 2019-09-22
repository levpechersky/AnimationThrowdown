import xml.etree.ElementTree as ET
from collections import defaultdict
from utils import *
from game import *


class GameDB:
	def __init__(self, cards_xmls, combos_xml, char_combos_xml):
		self.cards_xmls = cards_xmls
		self.combos_xml = combos_xml
		self.char_combos_xml = char_combos_xml

		# self.cards_by_rarity[raraity][name] -> CardProto
		self.cards_by_rarity = {}
		for rarity in Rarity:
			self.cards_by_rarity[rarity] = {}
		# self.cards_by_id[id] -> CardProto
		self.cards_by_id = {}
		# self.combos[id1][id2] -> CardProto  (id1 and id2 in any order - stored twice)
		self.combos = defaultdict(dict)
		# self.characters[internal_name] -> [CardProto...]
		self.characters = defaultdict(list)

	def load(self):
		new_part("PARSING GAME CARDS XML")

		for cards_xml in self.cards_xmls:
			print("Parsing cards data from {}".format(cards_xml))
			self._parse_cards(cards_xml)

		print("Parsing combos from {}".format(self.combos_xml))
		self._parse_combos(self.combos_xml)

		print("Parsing character combos from {}".format(self.combos_xml))
		self._parse_char_combos(self.char_combos_xml)

		# divide by 2 because we store each combo twice: [id1,id2] and [id2,id1]
		n_combos = sum([len(card_combos) for card_combos in self.combos.values()]) // 2
		print("Successfully loaded {} cards and {} combos from game XML files".format(len(self.cards_by_id), n_combos))

	def _parse_cards(self, path):
		xml = ET.parse(path)
		root = xml.getroot()
		for unit in root.findall('unit'):
			c = CardProto()

			# Internal, not playable cards
			if unit.find('commander') is not None:
				continue

			# Common fields
			c.id = int(unit.find('id').text)
			c.name = unit.find('name').text
			c.rarity = Rarity(int(unit.find('rarity').text))

			# Optional fields
			if unit.find('trait') is not None:
				c.trait = unit.find('trait').text
			if unit.find('health') is not None:
				c.hp = int(unit.find('health').text)
			if unit.find('attack') is not None:
				c.attack = int(unit.find('attack').text)
			if unit.find('health_multiplier') is not None:
				c.m_hp = float(unit.find('health_multiplier').text)
			if unit.find('attack_multiplier') is not None:
				c.m_attack = float(unit.find('attack_multiplier').text)

			for skill in unit.findall('skill'):
				s = self._parse_skill(skill)
				c.skills[s.id] = s

			for upgrade in unit.findall('upgrade'):
				c.upgrades.append(self._parse_upgrade(upgrade))

			# Type-specific:
			if unit.find('character') is not None:
				c.type = Type.HERO
			elif is_power_card(c.id):
				c.type = Type.POWER
			elif unit.findall('upgrade') is None:
				c.type = Type.COMBO
			else:
				c.type = Type.OBJECT

			c.series = c.get_series()

			debug(c)

			if unit.find('character') is not None:
				internal_name = unit.find('character').text
				self.characters[internal_name].append(c)
			self.cards_by_rarity[c.rarity][c.name] = c
			self.cards_by_id[c.id] = c

	def _parse_skill(self, skill):
		s = Skill()
		s.id = skill.get('id')
		# some of those may be None
		s.p = int(skill.get('p') or 0)
		s.v = int(skill.get('v') or 0)
		s.x = int(skill.get('x') or 0)
		s.y = skill.get('y')
		return s

	def _parse_upgrade(self, upgrade):
		u = Upgrade()
		u.level = int(upgrade.find('level').text)

		hp = upgrade.find('health')
		if hp is not None:
			u.hp = int(hp.text)

		at = upgrade.find('attack')
		if at is not None:
			u.attack = int(at.text)

		for skill in upgrade.findall('skill'):
			s = self._parse_skill(skill)
			u.skills[s.id] = s

		return u

	def _parse_combos(self, path):
		xml = ET.parse(path)
		root = xml.getroot()
		for combo in root.findall('combo'):
			cards = combo.find('cards')
			id = int(combo.find('card_id').text)
			c1 = int(cards.get('card1'))
			c2 = int(cards.get('card2'))
			card_proto = self.cards_by_id[id]
			self.combos[c1][c2] = card_proto
			self.combos[c2][c1] = card_proto

	def _parse_char_combos(self, path):
		xml = ET.parse(path)
		root = xml.getroot()
		for char in root.findall('character'):
			internal_name = char.find('name').text
			char_protos = self.characters[internal_name]
			for combo in char.findall('combo'):
				for proto in char_protos:
					c1 = proto.id
					c2 = int(combo.get('card'))
					combo_id = int(combo.get('output'))
					card_proto = self.cards_by_id[combo_id]
					self.combos[c1][c2] = card_proto
					self.combos[c2][c1] = card_proto

	def instantiate(self, rarity, name, level):
		proto = self.cards_by_rarity[rarity][name]
		return proto.get_instance(level)

	# return None if no such combo exists
	def combo_of(self, id1, id2):
		try:
			return self.combos[id1][id2]
		except KeyError:
			return None
