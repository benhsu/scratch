#!/usr/bin/env python
''' Markov-chain text generator	 Copyright 2011 Cheng Zhang '''
# import random, re, sys
import sys
from collections import deque, defaultdict

order = 4
fnin = "input.txt" # input text
mapsfrom = deque([" "] * order, maxlen=order) # the words currently the left hand of the transition
mapping = defaultdict(list) # key = a pickled representation of mapsfrom, value = a list of all encountared words with k as prefix. note this has to be a list not a hashmap since frequencies matter!

# def gen(n):
#		prefix = deque([" "] * order) # clear prefix
#		for i in range(n):
#			w = random.choice( sufdict['#'.join(prefix)] )
#			if w == " ": break
#			print w,
#			prefix.popleft()
#			prefix.append(w)

def gen(n):
	cur = deque([" "] * order, maxlen=order)
	from random import choice
	out = []
	for i in range(n):
		possiblilities = mapping["#".join(cur)]
		chosen = choice(possiblilities)
		cur.append(chosen)
		out.append(chosen)
	print " ".join(out)

def construct(lines):
	for l in lines:
		for w in l.strip().split():
			mapping["#".join(mapsfrom)].append(w)
			mapsfrom.append(w)

if __name__ == "__main__":
	# read and treat input file
	if len(sys.argv) > 1: fnin = sys.argv[1]
	inp = open(fnin).read()
	datars = open(fnin).readlines()
	construct(datars)
	gen(1500)

	# for s in inp.split(): add(s) # build Markov chain
	# add(" ")
	# gen(1500)
