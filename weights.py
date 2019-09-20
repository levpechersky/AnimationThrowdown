# All weights are per 1 unit of skill/hp/attack
# E.g. if Bobby has Punch=6, and Punch weight is 10, then total Punch weight is 60

HP_WEIGHT = 25

ATTACK_WEIGHT = 75

SKILL_WEIGHTS = {
	# Damage
	"Punch": 100,
	"Bomb": 95,
	"Crazed": 95,
	"Gas": 80,
	# Buff other
	"Give": 45,
	"Cheer": 45,
	"Cheer All": 75,
	"Motivate": 75,  # +attack for neigbors
	"Heal": 75,
	"Heal All": 95,
	# Debuff
	"Cripple": 60,
	"Cripple All": 90,
	# Defensive
	"Bodyguard": 75,  # fence
	"Sturdy": 60,  # brick wall
	"Shield": 65,
	"Shield All": 90,
	"Payback": 60,
	# Self-buff
	"Boost": 70,  # + attack on combo
	"Recover": 60,  # +hp on combo
	"Hijack": 60,
	"Leech": 55,  # heal when dealing damage
	"Jab": 45,  # piercing damage
}

####################################################

SINGLE_CARD_SCORE_WEIGHT = 10

COMBOS_SCORE_WEIGHT = 15
