#!/usr/bin/env python3

# Add parent directory to module search path in an ugly hack
import sys, os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import collections

from common import nn
import game
import player_nn_numpy
import player_random

def main():
	for _ in range(100):
		ws = []
		for _ in range(1000):
			w = game.run_game(player_random, player_nn_numpy, verbose=False)
			ws.append(w)
		print(collections.Counter(ws))

if __name__ == '__main__':
	main()
