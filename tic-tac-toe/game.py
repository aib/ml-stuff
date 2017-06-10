import tictactoe

INVALID_MOVE_CAUSES_LOSS = True

def run_game(p1m, p2m, verbose=False):
	board = tictactoe.Board()
	players = {
		board.players[0]: p1m.create_player(board, board.players[0]),
		board.players[1]: p2m.create_player(board, board.players[1])
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
			if moved:
				break
			elif INVALID_MOVE_CAUSES_LOSS:
				if verbose:
					print(board.to_play(), "has been eliminated by an invalid move")
				board.eliminate(board.to_play())
				break

		winner = board.winner()

	if verbose:
		print(board.draw(), end="")
		print("* Winner is", winner)
		print()

	for player in players.values():
		if callable(getattr(player, 'result', None)):
			player.result(board, winner)

	p1m.destroy_player(players[board.original_players[0]])
	p2m.destroy_player(players[board.original_players[1]])

	return winner
