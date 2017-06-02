#!/usr/bin/env python3

import tictactoe

import importlib
import os
import random
import re

def run_game(p1m, p2m, verbose=False):
	board = tictactoe.Board()
	players = {
		board.players[0]: p1m.create_player(board, board.players[0]),
		board.players[1]: p2m.create_player(board, board.players[0])
	}

	if verbose:
		print("* New game between:")
		for p in board.players:
			print("%s: %s" % (p, players[p]))
		print()

	winner = None
	while winner is None:
		if verbose:
			print(board.draw(), end="")
			print("%s (%s) to move" % (board.to_play(), players[board.to_play()]))
			print()

		# do-while or even a goto would help here...
		while True:
			move = players[board.to_play()].play(board)
			moved = board.play(move[0], move[1])
			if moved: break

		winner = board.winner()

	if verbose:
		print(board.draw(), end="")
		print("* Winner is", winner)
		print()

	for player in players.values():
		if callable(getattr(player, 'result', None)):
			player.result(board, winner)

	p1m.destroy_player(players[board.players[0]])
	p2m.destroy_player(players[board.players[1]])

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
