#!/usr/bin/python3

import random
import copy
import sys
from collections import namedtuple
import matplotlib as mpl
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

Card = namedtuple("Card", ['attack', 'hp', 'skill', 'skill_value'])


def random_cards(stat1, stat2):
	a = random.randint(5, 20)
	h = random.randint(10, 50)

	a1, h1, a2, h2 = 0, 0, 0, 0

	value = random.randint(1, 10)
	if stat1 == "HP":
		h1 = value
	elif stat1 == "Attack":
		a1 = value
	elif stat2 == "HP":
		h2 = value
	elif stat2 == "Attack":
		a2 = value

	c1 = Card(attack=a + a1, hp=h + h1, skill=stat1, skill_value=value)
	c2 = Card(attack=a + a2, hp=h + h2, skill=stat2, skill_value=value)

	return c1, c2




def get_choice(i_str):
	try:
		choice = input(i_str)
	except EOFError:
		show_graph()
		sys.exit(0)
	try:
		return int(choice)
	except ValueError:
		return 0


nodes = ["HP", "Attack", "Punch", "Bomb", "Crazed", "Gas", "Give", "Cheer", "Cheer All", "Motivate", "Heal", "Heal All", "Cripple", "Cripple All", "Bodyguard", "Sturdy", "Shield", "Shield All",
		 "Payback", "Boost", "Recover", "Hijack", "Leech", "Jab"]

SKILL_HINTS = {
	"Motivate": "+attack for neigbors",
	"Bodyguard": "fence",
	"Sturdy": "brick wall",
	"Boost": "+ attack on combo",
	"Recover": "+hp on combo",
	"Hijack": "steal",
	"Leech": "heal when dealing damage",
	"Jab": "piercing damage",
}


def cmp(s1, s2):
	c1, c2 = random_cards(s1, s2)

	i_str = "# 1: {:2}/{:2} card with {}({}) {}\n# 2: {:2}/{:2} card with {}({}) {}\n# "\
		.format(c1.attack, c1.hp, c1.skill, c1.skill_value, SKILL_HINTS.get(c1.skill) or "", c2.attack, c2.hp, c2.skill, c2.skill_value, SKILL_HINTS.get(c2.skill) or "")

	choice = get_choice(i_str)
	while choice not in [0, 1, 2]:
		print("# Please, enter 1 or 2 to choose, or 0 to skip")
		choice = get_choice(i_str)

	if choice == 1:
		return -1
	if choice == 2:
		return 1

	return 0


# This function takes last element as pivot, places
# the pivot element at its correct position in sorted
# array, and places all smaller (smaller than pivot)
# to left of pivot and all greater elements to right
# of pivot
def partition(arr, low, high):
	i = (low - 1)  # index of smaller element
	pivot = arr[high]  # pivot

	for j in range(low, high):

		# If current element is smaller than or
		# equal to pivot
		if cmp(arr[j], pivot) <= 0:
			# increment index of smaller element
			i = i + 1
			arr[i], arr[j] = arr[j], arr[i]

	arr[i + 1], arr[high] = arr[high], arr[i + 1]
	return (i + 1)


# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low  --> Starting index,
# high  --> Ending index

# Function to do Quick sort
def quickSort(arr, low, high):
	if low < high:
		# pi is partitioning index, arr[p] is now
		# at right place
		pi = partition(arr, low, high)

		# Separately sort elements before
		# partition and after partition
		quickSort(arr, low, pi - 1)
		quickSort(arr, pi + 1, high)


quickSort(nodes, 0, len(nodes)-1)
print(nodes)
exit()


import networkx as nx


def show_graph():
	pos = nx.layout.spring_layout(G)
	nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_color='blue', node_size=1)
	nx.draw_networkx_labels(G, pos)
	nx.draw_networkx_edges(G, pos, edge_color='red', arrows=True)
	# plt.show() # TODO

	path = "test.graphml"
	nx.write_graphml(G, path)

	# TODO: remove attributes from source graphml

	oxml = ET.Element('graphml')

	xml = ET.parse(path)
	root = ET.Element
	root = xml.getroot()
	graph = root.find('graph')

	g = ET.Element('graph')
	oxml.append(g)
	g.set('id', 'Graph')
	g.set('uidGraph', str(G.number_of_nodes() + 1))
	g.set('uidEdge', '10001')

	uids = {}

	nodes = ET.Element('nodes')
	g.append(nodes)
	for i, edge in enumerate(graph.findall('node')):
		text_id = edge.get('id')
		uids[text_id] = i

		n = ET.Element('node')
		nodes.append(n)
		n.set('id', str(i))
		n.set('positionX', str(random.randint(0, 500)))
		n.set('positionY', str(random.randint(0, 500)))
		n.set('mainText', text_id)
		n.set('upText', '')

	edges = ET.Element('edges')
	g.append(edges)
	for i, edge in enumerate(graph.findall('edge')):
		id = i + 10000
		src = edge.get('source')
		dst = edge.get('target')

		e = ET.Element('edge')
		edges.append(e)
		e.set('id', str(id))
		e.set('vertex1', str(uids[src]))
		e.set('vertex2', str(uids[dst]))
		e.set('isDirect', 'true')
		e.set('weight', '1')
		e.set('useWeight', 'false')
		e.set('hasPair', 'false')
		e.set('text', '')
		e.set('arrayStyleStart', '')
		e.set('arrayStyleFinish', '')
		e.set('model_width', '4')
		e.set('model_type', '0')
		e.set('model_curvedValue', '0.1')

	ET.dump(oxml)


G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edge("Heal All", "Heal")
G.add_edge("Cripple All", "Cripple")
G.add_edge("Cheer All", "Cheer")
G.add_edge("Shield All", "Shield")
G.add_edge("Attack", "HP")

# Load from previous input.
import weights_gen_cache
weights_gen_cache.set_w(G)

nodes2 = copy.copy(nodes)
random.shuffle(nodes)

print("# What would you prefer? (1 or 2 to choose, or 0 to skip)")
for n1 in nodes:
	print("#")
	print("#")
	n2 = random.choice(nodes2)
	nodes2.remove(n2)
	if n1 == n2:
		continue
	if G.has_edge(n1, n2) or G.has_edge(n2, n1):
		continue

	c1, c2 = random_cards(n1, n2)

	i_str = "# 1: {:2}/{:2} card with {}({}) {}\n# 2: {:2}/{:2} card with {}({}) {}\n# "\
		.format(c1.attack, c1.hp, c1.skill, c1.skill_value, SKILL_HINTS.get(c1.skill) or "", c2.attack, c2.hp, c2.skill, c2.skill_value, SKILL_HINTS.get(c2.skill) or "")

	choice = get_choice(i_str)
	while choice not in [0, 1, 2]:
		print("# Please, enter 1 or 2 to choose, or 0 to skip")
		choice = get_choice(i_str)

	if choice == 1:
		G.add_edge(n1, n2)
		print('G.add_edge("{}", "{}")'.format(n1, n2))
	if choice == 2:
		G.add_edge(n2, n1)
		print('G.add_edge("{}", "{}")'.format(n2, n1))

show_graph()
