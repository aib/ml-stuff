#!/usr/bin/env python3

# Add parent directory to module search path in an ugly hack
import sys, os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import importlib
import os
import random
import re

import game

def load_player_modules():
	player_modules = {}

	for fn in os.listdir('.'):
		if not os.path.isfile(fn):
			continue

		m = re.match(r'^player_([a-zA-Z_]+).py$', fn)
		if m is None:
			continue

		name = m.group(1)
		module = importlib.import_module('player_' + name)
		player_modules[name] = module

	return player_modules

def main():
	player_modules = load_player_modules()

	p1m = random.choice(list(player_modules.values()))
	p2m = random.choice(list(player_modules.values()))
	w = game.run_game(p1m, p2m, verbose=True)

if __name__ == '__main__':
	main()
