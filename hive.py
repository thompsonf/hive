import random

dir_E = (1, 0)
dir_NE = (1, -1)
dir_SE = (0, 1)
dir_SW = (-1, 1)
dir_W = (-1, 0)
dir_NW = (0, -1)

dirs = [dir_E, dir_NE, dir_SE, dir_SW, dir_W, dir_NW]

board = {}

def add_coords(c1, c2):
	return (c1[0] + c2[0], c1[1] + c2[1])

#test whether board is connected if a certain piece is moved
#uses depth-first search
def is_board_connected_except_coords(removed_coords):
	coord_list = set(board.keys())
	coord_list.remove(removed_coords)
	stack = [random.sample(coord_list, 1)[-1]]
	discovered = set()
	while stack:
		coords = stack.pop()
		if coords not in discovered:
			discovered.add(coords)
			for test_dir in dirs:
				test_coords = add_coords(coords, test_dir)
				if test_coords in coord_list and test_coords not in discovered: #is not in discovered necessary? Don't use it on wikipedia
					stack.append(test_coords)
	return discovered == coord_list


def can_be_inserted(coords, color):
	is_neighbor_of_some_piece = False
	for test_dir in dirs:
		test_coords = add_coords(coords, test_dir)
		if test_coords in board:
			if board[test_coords][-1].color != color:
				return False
			is_neighbor_of_some_piece = True
	return is_neighbor_of_some_piece

class Bug:
	def __init__(self, coords, color):
		self.coords = coords
		self.color = color
		self.height = 1

	def move(self, new_coords):
		if new_coords in board:
			board[new_coords].append(self)
		else:
			board[new_coords] = [self]
		board[self.coords].pop()
		if not board[self.coords]:
			board.pop(self.coords, None)
		self.coords = new_coords
		self.height = len(board[new_coords])

	def isValidMove(self, new_coords):
		return new_coords in self.getValidMoves()

class Queen(Bug):
	#remember to test whether board remains connected!
	def getValidMoves(self):
		valid_moves = set()
		if self.height != len(board[self.coords]):
			return valid_moves 
		for main_dir_idx in range(len(dirs)):
			off_dir_idx1 = (main_dir_idx + 1) % 6
			off_dir_idx2 = (main_dir_idx - 1) % 6
			
			main_dir_coords = add_coords(self.coords, dirs[main_dir_idx])
			off_dir_coords1 = add_coords(self.coords, dirs[off_dir_idx1])
			off_dir_coords2 = add_coords(self.coords, dirs[off_dir_idx2])

			if main_dir_coords not in board and (off_dir_coords1 not in board or off_dir_coords2 not in board) and :
				valid_moves.add(main_dir_coords)
		return valid_moves

# board[(0,0)] = [Queen((0,0), 'w')]
# board[(1,0)] = [Queen((1,0), 'b')]
# board[(1,1)] = [Queen((1,1), 'w')]

hexes = [(0,0), (1,0), (2,0), (1,-1), (1, -2)]
board = {x:0 for x in hexes}
for coords in board.keys():
	print(coords, is_board_connected_except_coords(coords))