# tic-tac-toe (X/O) game!
import numpy as np
import random

X = 'X'
O = 'O'  # the two players
#_XO = {1: 'X', 0: 'O'}

SIDE = 5
WIN_SIZE = 3
# that's the standard game, but the code works for any choice of WIN_SIZE <= SIDE :)
# could be SIDE = 7 and WIN-SIZE = 4 for instace, for a 7x7 board where a row/col/diagonal of length 4 is a winner.

class xo_game(object):

	@staticmethod
	def is_row_win_move(b_row, player, col):
		# checks whether the current move was a winning one in b_row (which is an array of length SIDE)
		size = min(SIDE, len(b_row))  					# maybe we got a partial "row" - happens in case of diagonals
		range_min = max(0, col - WIN_SIZE +1)			# lowest relevant col index
		range_max = min(col + WIN_SIZE - 1, size-1)		# highest relevant col index

		# we first check how far can we go on the left, then go to right if that was not enough good cells (remembering the left):
		# with each found good sign (X/O) we reduce "remains" by 1, till it gets to zero
		
		remains = WIN_SIZE - 1  # we already have one, which is the current move of the player
		# CHECK on the LEFT:
		i = col  # the move column (out starting point)
		still_good = True
		while still_good and (i > range_min) and (remains > 0):  # last condition is not really needed
			i -= 1  # move one to the left
			if (b_row[[i]] == player):
				remains -= 1  # gained one point, this many to go!
			else:
				still_good = False
		if (remains == 0):
			return True
		
		# else, CHECK on the RIGHT:
		i = col
		still_good = True
		while still_good and (i < range_max) and (remains > 0):
			i += 1
			if (b_row[[i]] == player):
				remains -= 1
			else:
				still_good = False
		if (remains == 0):
			return True
		else:
			return False


	def __init__(self, board = None, state = 'playing'):
		# the current/initialized board, should be an 3x3 matrix of strings
		if board == None:
			self.board = self.new_game()
		else:
			self.board = board

		# current state of the game: "playing", "X won", "O won", "tie"
		self.state = state

	def play(self, player, move):
		""" 
		Changes the board state according to the player and move: 
		player is 'O' or 'X', move is a location in the array = (row, col) is a *tuple*.
		If the move is not valid, prints a warning and returns False, otherwise modified the board and returns True."""
		# TODO: check is move is valid! #
		self.board[move] = player

	def move_result(self, player, move):
		# check whether is was a winning move or we're still playing, OR it's the end without winner
		(row, col) = move
		offset = col-row
		main_diag = np.diagonal(self.board, offset)
		new_col = SIDE - col - 1  # new_row = row with vertical mirror
		scnd_offset = new_col - row	
		scnd_diag = np.diagonal(np.fliplr(self.board), scnd_offset)  # using vertical "mirror"

		print("the row tested is ", self.board[row,:], "with internal current cell index", col)
		print("the col tested is ", self.board[:,col], "with internal current cell index", row)
		print("main diag tested is ", main_diag, "with internal current cell index", col if offset<0 else row)
		print("sec diag tested is ", scnd_diag, "with internal current cell index", new_col if scnd_offset<0 else row)

		if self.is_row_win_move(self.board[row,:], player, col):  # row victory?
			print("row victory!")
			return True
		elif self.is_row_win_move(self.board[:,col], player, row):  # col victory?
			print("col victory!")
			return True
		elif (len(main_diag)>= WIN_SIZE) and self.is_row_win_move(main_diag, player, col if offset<0 else row) : 
			# main diagonal victory  
			#BTW, col = row + offset
			print("main diagonal victory!")
			return True
		elif (len(scnd_diag) >= WIN_SIZE) and self.is_row_win_move(scnd_diag, player, new_col if scnd_offset<0 else row) :
			# secondary diagonal victory!
			print("secondary diagonal victory!")
			return True 
		else:
			return False

	def game_state(self):
		# checks if game is over/won or still playing
		return 'playing'  # for now

	def new_game(self):  # initializes to an empty board
		return np.empty([SIDE,SIDE], dtype = str)

	def display(self):  # prints the board
		print("\n")
		print(self.board)

# NOTE: we actually don't need to know which player is now, because we can count have many turns were taken and conclude whos turn it's now.
# But, for convenience and readability, let's leave it like that for now, explicitely providing 'X' or 'O'.

#class Match(object):


def generate_random_move(board):
	""" Returns a (valid) random move on the given board."""
	vacant = np.argwhere(board == '')  # finding indices of empty cells
	rand_ind = random.randrange(0, len(vacant))  # generating a random index
	move = tuple(vacant[rand_ind])  # taking random vacant place

	return move


def smart_move(board, player):
	""" Runs some in-depth inspection and returns "the best" move for a given player."""
	return True

def reinforced_move(board, player):
	# big plans..
	return True


def random_player():
	""" a player that always plays randomely"""
	return True



b = xo_game()
# print(b.board.shape)
# move = (1,0)
# b.play(X, move)
# b.display()
# print(b.move_result(X, move))
# move = (1, 1)
# print('sanity: ', (b.board[(1,0)]))
# b.play(X, move)
# print(b.move_result(X, move))

#b.play('O', (0,1))

i = 0
game_won = False
while i<20 and not game_won:
	player = X if (i%2 == 0) else O  # staring with 0, so even i is actually X
	print("\nNow playing: ", player)
	move = generate_random_move(b.board)
	b.play(player, move)
	b.display()
	game_won = b.move_result(player, move)
	if game_won:
		print(player, "won!")
	i += 1
if not game_won: print("It's a tie.")
