coins = 5
cards = 7

def avg():
		return 5.0*float(coins)/cards

def copper():
		global coins
		global cards
		coins = coins + 1
		cards = cards + 1

def silver():
		global coins
		global cards
		coins = coins + 2
		cards = cards + 1

def gold():
		global coins
		global cards
		coins = coins + 3
		cards = cards + 1

def trash():
	global cards
	cards = cards - 4

def province():
	global cards
	cards = cards + 1

silver()
print avg()
silver()
print avg()
copper()
print avg()
copper()
print avg()
copper()
print avg()
copper()
print avg()
copper()
print avg()
copper()
print avg()
copper()
print avg()
copper()
print avg()
