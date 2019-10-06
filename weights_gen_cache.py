
def set_w(G):
	# What would you prefer? (1 or 2 to choose, or 0 to skip)
	#
	#
	# 1: 10/46 card with Give(10)
	# 2: 10/46 card with Sturdy(10) brick wall
	# 2
	G.add_edge("Sturdy", "Give")
	#
	#
	# 1: 12/18 card with Motivate(10) +attack for neigbors
	# 2: 12/18 card with Recover(10) +hp on combo
	# 1
	G.add_edge("Motivate", "Recover")
	#
	#
	# 1: 19/30 card with Cheer All(10)
	# 2: 19/30 card with Leech(10) heal when dealing damage
	# 1
	G.add_edge("Cheer All", "Leech")
	#
	#
	# 1: 11/49 card with Sturdy(10) brick wall
	# 2: 11/59 card with HP(10)
	# 1
	G.add_edge("Sturdy", "HP")
	#
	#
	#
	#
	# 1: 20/44 card with Shield All(10)
	# 2: 20/44 card with Punch(10)
	# 11
	# Please, enter 1 or 2 to choose, or 0 to skip
	# 1: 20/44 card with Shield All(10)
	# 2: 20/44 card with Punch(10)
	# 1
	G.add_edge("Shield All", "Punch")
	#
	#
	# 1: 10/30 card with Leech(6) heal when dealing damage
	# 2: 10/30 card with Bodyguard(6) fence
	# 2
	G.add_edge("Bodyguard", "Leech")
	#
	#
	# 1:  8/28 card with Bodyguard(6) fence
	# 2:  8/28 card with Motivate(6) +attack for neigbors
	# 2
	G.add_edge("Motivate", "Bodyguard")
	#
	#
	# 1:  8/36 card with Shield(10)
	# 2:  8/36 card with Jab(10) piercing damage
	# 1
	G.add_edge("Shield", "Jab")
	#
	#
	# 1: 17/17 card with Payback(4)
	# 2: 17/17 card with Hijack(4) steal
	# 0
	#
	#
	# 1: 16/13 card with Heal(4)
	# 2: 16/13 card with Shield(4)
	# 1
	G.add_edge("Heal", "Shield")
	#
	#
	# 1: 12/14 card with Jab(4) piercing damage
	# 2: 12/14 card with Cripple(4)
	# 2
	G.add_edge("Cripple", "Jab")
	#
	#
	# 1:  9/15 card with Cheer(9)
	# 2:  9/15 card with Shield All(9)
	# 2
	G.add_edge("Shield All", "Cheer")
	#
	#
	# 1:  9/30 card with Cripple(1)
	# 2:  9/30 card with Heal(1)
	# 2
	G.add_edge("Heal", "Cripple")
	#
	#
	# 1: 14/36 card with Punch(6)
	# 2: 14/36 card with Heal All(6)
	# 2
	G.add_edge("Heal All", "Punch")
	#
	#
	# 1: 11/30 card with HP(8)
	# 2: 11/22 card with Bomb(8)
	# 2
	G.add_edge("Bomb", "HP")
	#
	#
	# 1: 14/15 card with Gas(5)
	# 2: 14/15 card with Cripple All(5)
	# 2
	G.add_edge("Cripple All", "Gas")
	#
	#
	# 1: 13/47 card with Heal All(2)
	# 2: 13/47 card with Cheer All(2)
	# 1
	G.add_edge("Heal All", "Cheer All")
	#
	#
	# 1:  5/36 card with Bomb(8)
	# 2:  5/36 card with Payback(8)
	# 1
	G.add_edge("Bomb", "Payback")
	#
	#
	# 1: 14/30 card with Recover(7) +hp on combo
	# 2: 14/30 card with Cheer(7)
	# 1
	G.add_edge("Recover", "Cheer")
	#
	#
	#
	#
	#
	#
	# 1:  8/37 card with Hijack(4) steal
	# 2:  8/37 card with Boost(4) + attack on combo
	# 2
	G.add_edge("Boost", "Hijack")
	#
	#
	# 1: 13/10 card with Boost(2) + attack on combo
	# 2: 13/10 card with Give(2)
	# 1
	G.add_edge("Boost", "Give")

	# What would you prefer? (1 or 2 to choose, or 0 to skip)
	#
	#
	# 1:  9/18 card with Cripple All(7)
	# 2:  9/25 card with HP(7)
	# 1
	G.add_edge("Cripple All", "HP")
	#
	#
	#
	#
	# 1:  6/24 card with Recover(3) +hp on combo
	# 2:  6/24 card with Payback(3)
	# 1
	G.add_edge("Recover", "Payback")
	#
	#
	# 1: 20/19 card with Heal(4)
	# 2: 20/19 card with Leech(4) heal when dealing damage
	# 1
	G.add_edge("Heal", "Leech")
	#
	#
	# 1: 12/31 card with Leech(3) heal when dealing damage
	# 2: 12/31 card with Gas(3)
	# 2
	G.add_edge("Gas", "Leech")
	#
	#
	# 1: 17/51 card with HP(8)
	# 2: 17/43 card with Shield(8)
	#
	# What would you prefer? (1 or 2 to choose, or 0 to skip)
	#
	#
	# 1:  9/18 card with Cripple All(7)
	# 2:  9/25 card with HP(7)
	# 1
	G.add_edge("Cripple All", "HP")
	#
	#
	#
	#
	# 1:  6/24 card with Recover(3) +hp on combo
	# 2:  6/24 card with Payback(3)
	# 1
	G.add_edge("Recover", "Payback")
	#
	#
	# 1: 20/19 card with Heal(4)
	# 2: 20/19 card with Leech(4) heal when dealing damage
	# 1
	G.add_edge("Heal", "Leech")
	#
	#
	# 1: 12/31 card with Leech(3) heal when dealing damage
	# 2: 12/31 card with Gas(3)
	# 2
	G.add_edge("Gas", "Leech")
	#
	#
	# 1: 17/51 card with HP(8)
	# 2: 17/43 card with Shield(8)
	#

	# What would you prefer? (1 or 2 to choose, or 0 to skip)
	#
	#
	# 1:  9/46 card with Cheer(2)
	# 2:  9/46 card with Hijack(2) steal
	# 0
	#
	#
	# 1: 20/50 card with Leech(8) heal when dealing damage
	# 2: 20/50 card with Heal All(8)
	# 2
	G.add_edge("Heal All", "Leech")
	#
	#
	# 1: 12/37 card with HP(8)
	# 2: 12/29 card with Punch(8)
	# 2
	G.add_edge("Punch", "HP")
	#
	#
	# 1:  6/31 card with Shield All(5)
	# 2:  6/31 card with Crazed(5)
	# 1
	G.add_edge("Shield All", "Crazed")
	#
	#
	# 1: 20/16 card with Crazed(1)
	# 2: 20/16 card with Recover(1) +hp on combo
	# 1
	G.add_edge("Crazed", "Recover")
	#
	#
	# 1: 25/16 card with Attack(9)
	# 2: 16/16 card with Shield(9)
	# 1
	G.add_edge("Attack", "Shield")
	#
	#
	# 1:  5/12 card with Sturdy(3) brick wall
	# 2:  5/12 card with Bomb(3)
	# 2
	G.add_edge("Bomb", "Sturdy")
	#
	#
	# 1: 17/41 card with Shield(5)
	# 2: 17/41 card with Boost(5) + attack on combo
	# 2
	G.add_edge("Boost", "Shield")
	#
	#
	# 1: 18/33 card with Gas(6)
	# 2: 18/33 card with Bodyguard(6) fence
	# 2
	G.add_edge("Bodyguard", "Gas")
	#
	#
	# 1: 13/26 card with Cripple All(9)
	# 2: 13/26 card with Cheer All(9)
	# 1
	G.add_edge("Cripple All", "Cheer All")
	#
	#
	# 1: 17/28 card with Cripple(8)
	# 2: 17/28 card with Payback(8)
	# 1
	G.add_edge("Cripple", "Payback")
	#
	#
	# 1: 17/13 card with Cheer All(8)
	# 2: 17/13 card with Sturdy(8) brick wall
	# 1
	G.add_edge("Cheer All", "Sturdy")
	#
	#
	# 1: 15/20 card with Bomb(5)
	# 2: 15/20 card with Leech(5) heal when dealing damage
	# 1
	G.add_edge("Bomb", "Leech")
	#
	#
	# 1:  9/10 card with Recover(2) +hp on combo
	# 2:  9/10 card with Shield All(2)
	# 2
	G.add_edge("Shield All", "Recover")
	#
	#
	# 1: 12/29 card with Jab(10) piercing damage
	# 2: 12/29 card with Motivate(10) +attack for neigbors
	# 2
	G.add_edge("Motivate", "Jab")
	#
	#
	# 1: 14/50 card with Heal All(6)
	# 2: 14/50 card with Cripple(6)
	# 1
	G.add_edge("Heal All", "Cripple")
	#
	#
	# 1: 20/46 card with Boost(3) + attack on combo
	# 2: 20/46 card with Jab(3) piercing damage
	# 1
	G.add_edge("Boost", "Jab")
	#
	#
	# 1: 13/45 card with Bodyguard(9) fence
	# 2: 13/45 card with Cripple All(9)
	# 2
	G.add_edge("Cripple All", "Bodyguard")
	#
	#
	# 1: 16/21 card with Give(3)
	# 2: 16/21 card with Heal(3)
	# 2
	G.add_edge("Heal", "Give")
	#
	#
	# 1: 11/27 card with Hijack(4) steal
	# 2: 11/27 card with Give(4)
	# 0
	#
	#
	# 1:  5/16 card with Heal(6)
	# 2:  5/16 card with Gas(6)
	# 1
	G.add_edge("Heal", "Gas")
	#
	#
	# 1:  6/36 card with Punch(1)
	# 2:  6/36 card with Cheer(1)
	# 1
	G.add_edge("Punch", "Cheer")
	#
	#
	# 1:  7/32 card with Payback(5)
	# 2:  7/37 card with HP(5)
	# 2
	G.add_edge("HP", "Payback")
	#
	#
	# 1: 11/10 card with Motivate(7) +attack for neigbors
	# 2: 18/10 card with Attack(7)
	# 0

	# What would you prefer? (1 or 2 to choose, or 0 to skip)
	#
	#
	# 1: 19/21 card with Gas(5)
	# 2: 19/21 card with Cripple(5)
	# 1
	G.add_edge("Gas", "Cripple")
	#
	#
	# 1:  6/28 card with Heal All(5)
	# 2:  6/28 card with Crazed(5)
	# 1
	G.add_edge("Heal All", "Crazed")
	#
	#
	#
	#
	# 1: 20/17 card with Cheer(2)
	# 2: 20/17 card with Motivate(2) +attack for neigbors
	# 0
	#
	#
	# 1: 10/11 card with Crazed(10)
	# 2: 10/11 card with Punch(10)
	# 0
	#
	#
	# 1: 19/31 card with Boost(4) + attack on combo
	# 2: 19/31 card with Heal All(4)
	# 2
	G.add_edge("Heal All", "Boost")
	#
	#
	#
	#
	# 1: 11/37 card with Recover(8) +hp on combo
	# 2: 11/37 card with Heal(8)
	# 2
	G.add_edge("Heal", "Recover")
	#
	#
	# 1: 20/18 card with Hijack(7) steal
	# 2: 20/25 card with HP(7)
	# 2
	G.add_edge("HP", "Hijack")
	#
	#
	# 1:  9/19 card with Bodyguard(6) fence
	# 2:  9/19 card with Shield(6)
	# 1
	G.add_edge("Bodyguard", "Shield")
	#
	#
	# 1: 19/23 card with Give(3)
	# 2: 19/23 card with Cheer(3)
	# 0
	#
	#
	# 1: 20/42 card with Cripple(3)
	# 2: 20/42 card with Boost(3) + attack on combo
	# 0
	#
	#
	# 1: 18/20 card with Shield(9)
	# 2: 18/20 card with Cripple All(9)
	# 2
	G.add_edge("Cripple All", "Shield")
	#
	#
	#
	#
	# 1:  5/32 card with Heal(10)
	# 2:  5/32 card with Jab(10) piercing damage
	# 1
	G.add_edge("Heal", "Jab")
	#
	#
	# 1: 12/22 card with Sturdy(9) brick wall
	# 2: 12/22 card with Shield All(9)
	# 2
	G.add_edge("Shield All", "Sturdy")
	#
	#
	# 1: 17/24 card with Motivate(10) +attack for neigbors
	# 2: 17/24 card with Hijack(10) steal
	# 1
	G.add_edge("Motivate", "Hijack")
	#
	#
	# 1: 19/12 card with Jab(10) piercing damage
	# 2: 29/12 card with Attack(10)
	# 2
	G.add_edge("Attack", "Jab")
	#
	#
	# 1: 15/19 card with Shield All(9)
	# 2: 15/19 card with Give(9)
	# 1
	G.add_edge("Shield All", "Give")
	#
	#
	# 1: 19/34 card with Punch(4)
	# 2: 19/34 card with Sturdy(4) brick wall
	# 1
	G.add_edge("Punch", "Sturdy")
	#
	#
	#
	#
	# 1: 19/33 card with HP(3)
	# 2: 19/30 card with Leech(3) heal when dealing damage
	# 1
	G.add_edge("HP", "Leech")
	#
	#
	#
	#
	# 1: 12/34 card with Attack(7)
	# 2:  5/34 card with Bomb(7)
	# 0
