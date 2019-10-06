# All weights are per 1 unit of skill/hp/attack
# E.g. if Bobby has Punch=6, and Punch weight is 10, then total Punch weight is 60

HP_WEIGHT = 40

ATTACK_WEIGHT = 100

SKILL_WEIGHTS = {
	"Shield All": 90,
	"Heal All": 95,
	"Cripple All": 90,

	"Cheer All": 75,

	"Punch": 100,
	"Crazed": 95,
	"Motivate": 75,  # +attack for neigbors
	"Heal": 75,

	"Bomb": 100,
	"Boost": 100,  # + attack on combo
	# Attack

	"Bodyguard": 85,  # fence

	"Recover": 70,  # +hp on combo

	"Cripple": 60,
	"Sturdy": 60,  # brick wall
	"Gas": 60,

	"Give": 50,

	# HP

	"Cheer": 35,
	"Shield": 35,

	"Jab": 30,  # piercing damage

	"Payback": 25,
	"Hijack": 25,
	"Leech": 25,  # heal when dealing damage


	# WTF?
	"Burn": 60,
	"Enlarge": 60,
}

####################################################

SINGLE_CARD_SCORE_WEIGHT = 30

COMBOS_SCORE_WEIGHT = 20
