#!/usr/bin/env python3

import tictactoe

import importlib
import os
import random
import re

def run_game(p1m, p2m, verbose=False):
	board = tictactoe.Board()
	p1 = p1m.create_player(board)
	p2 = p2m.create_player(board)

	to_play = p1

	winner = None
	while winner is None:
		if verbose:
			print(board.draw(), end="")
			print("P1" if to_play == p1 else "P2", to_play, "to move")
			print()

		# do-while or even a goto would help here...
		while True:
			move = to_play.play(board)
			moved = board.play(move[0], move[1])
			if moved: break

		if to_play == p1:
			to_play = p2
		else:
			to_play = p1

		winner = board.winner()

	if verbose:
		print(board.draw(), end="")
		print("Winner is", winner)
		print()

	p1m.destroy_player(p1)
	p2m.destroy_player(p2)

	return winner

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
	w = run_game(p1m, p2m, verbose=True)

if __name__ == '__main__':
	main()
