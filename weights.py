import os
from utils import *
# All weights are per 1 unit of skill/hp/attack
# E.g. if Bobby has Punch=6, and Punch weight is 10, then total Punch weight is 60
#
# Values themselves don't matter much, the relation between weights is what matters.


W_HP_DEFAULT = 40
W_ATTACK_DEFAULT = 100
W_SKILL_DEFAULT = {
	"Punch": 100,
	"Bomb": 100,
	"Boost": 100,
	"Heal All": 95,
	"Crazed": 95,
	"Shield All": 90,
	"Cripple All": 90,
	"Bodyguard": 85,
	"Cheer All": 75,
	"Motivate": 75,
	"Heal": 75,
	"Recover": 70,
	"Cripple": 60,
	"Sturdy": 60,
	"Gas": 60,
	"Burn": 60,
	"Enlarge": 60,
	"Give": 50,
	"Cheer": 35,
	"Shield": 35,
	"Jab": 30,
	"Payback": 25,
	"Hijack": 25,
	"Leech": 25,
}

W_HP_AGGRESSIVE = 80
W_ATTACK_AGGRESSIVE = 130
W_SKILLS_AGGRESSIVE = {
	'Heal All': 190,
	'Cripple All': 190,
	'Shield All': 190,
	'Punch': 170,
	'Crazed': 160,
	'Motivate': 150,
	'Bomb': 150,
	'Attack': 130,
	'Cheer All': 120,
	'Heal': 120,
	'Bodyguard': 110,
	'Gas': 100,
	'Cripple': 100,
	'Burn': 100,
	'Enlarge': 100,
	'Boost': 90,
	'HP': 80,
	'Sturdy': 80,
	'Cheer': 70,
	'Recover': 70,
	'Shield': 70,
	'Payback': 60,
	'Leech': 50,
	'Hijack': 50,
	'Give': 50,
	'Jab': 40,
}

W_HP_GENERATED = 28
W_ATTACK_GENERATED = 100
W_SKILL_GENERATED = {
	'Cripple All': 185,
	'Shield All': 180,
	'Heal All': 171,
	'Motivate': 150,
	'Cheer All': 140,
	'Bomb': 135,
	'Punch': 125,
	'Crazed': 120,
	'Heal': 108,
	'Gas': 73,
	'Burn': 70,
	'Enlarge': 70,
	'Bodyguard': 66,
	'Boost': 66,
	'Sturdy': 64,
	'Cripple': 61,
	'Recover': 60,
	'Payback': 58,
	'Shield': 57,
	'Hijack': 50,
	'Cheer': 44,
	'Leech': 40,
	'Jab': 39,
	'Give': 37,
}
####################################################

SINGLE_CARD_SCORE_WEIGHT = 30
COMBOS_SCORE_WEIGHT = 20

HP_WEIGHT = W_HP_GENERATED
ATTACK_WEIGHT = W_ATTACK_GENERATED
SKILL_WEIGHTS = W_SKILL_GENERATED

if os.path.isfile(USER_WEIGHTS_FILE):
	print("User-defined skills weights file found: {}".format(USER_WEIGHTS_FILE))
	from weights_user import *
	print("Using user-defined skills weights file: {}".format(USER_WEIGHTS_FILE))
else:
	print("Using default skills weights")
