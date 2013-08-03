#!/usr/bin/env python
''' Markov-chain text generator  Copyright 2011 Cheng Zhang '''
# import random, re, sys
import sys
from flask import Flask, request, session, g, redirect, url_for,  abort, render_template, flash
from collections import deque, defaultdict

order = 1
fnin = "input.txt" # input text
mapsfrom = deque([" "] * order, maxlen=order) # the words currently the left hand of the transition
mapping = defaultdict(list) # key = a pickled representation of mapsfrom, value = a list of all encountared words with k as prefix. note this has to be a list not a hashmap since frequencies matter!
firsts = [] # list of all the first words in the lines
# default value seems to bethe first one there
app = Flask(__name__)

# def gen(n):
#   prefix = deque([" "] * order) # clear prefix
#   for i in range(n):
#     w = random.choice( sufdict['#'.join(prefix)] )
#     if w == " ": break
#     print w,
#     prefix.popleft()
#     prefix.append(w)

@app.route("/random")
def random():
  return gen(4)

def gen(n):
  from random import choice, seed
  seed()
  cur = deque([" "] * order, maxlen=order)
  cur.append(choice(firsts))
  # print cur
  out = []
  # print mapping
  for i in range(n):
    possiblilities = mapping["#".join(cur)]
    # print possiblilities
    if len(possiblilities)==0:
      chosen = [choice(mapsfrom)]
    else:
      chosen = choice(possiblilities)
    if chosen=="EOF":
      break
    cur.append(chosen)
    out.append(chosen)
  return " ".join(out).replace("_", " ")

def construct(lines):
  for l in lines:
    # hack: change "the " to "the_" and back again
    l = l.replace(" the ", " the_")
    firsts.append(l.strip().split()[0])
    for w in l.strip().split():
      # w = w.replace("the_", "the ")
      # print w
      mapping["#".join(mapsfrom)].append(w)
      mapsfrom.append(w)
    mapping[l.strip().split()[-1]].append("EOF")
  # print mapping
      
if __name__ == "__main__":
  # read and treat input file
  if len(sys.argv) > 1: fnin = sys.argv[1]
  inp = open(fnin).read()
  datars = open(fnin).readlines()
  # print datars
  construct(datars)
  app.run(host="0.0.0.0")
  # gen(4)

  # for s in inp.split(): add(s) # build Markov chain
  # add(" ")
  # gen(1500)
