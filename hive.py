import random
import math
from tkinter import *
from tkinter import ttk

dir_E = (1, 0)
dir_SE = (0, 1)
dir_SW = (-1, 1)
dir_W = (-1, 0)
dir_NW = (0, -1)
dir_NE = (1, -1)

dirs = [dir_E, dir_SE, dir_SW, dir_W, dir_NW, dir_NE]

board = {}

def display_board(size, selected_hex=None, valid_moves=set()):
	root = Tk()
	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)
	canvas = Canvas(root)
	canvas.grid(column=0, row=0, sticky=(N, W, E, S))
	canvas.configure(background='gray')

	all_hexes = set(board.keys())

	for axial_coords in all_hexes:
		vertices = get_unrolled_vertices_from_axial(axial_coords, size, (300, 300))
		if axial_coords != selected_hex:
			canvas.create_polygon(vertices, outline='black', fill='white', width=3)
		else:
			canvas.create_polygon(vertices, outline='black', fill='red', width=6)

	for axial_coords in valid_moves:
		vertices = get_unrolled_vertices_from_axial(axial_coords, size, (300, 300))
		canvas.create_polygon(vertices, outline='black', fill='green', width=1)

	root.mainloop()

def get_unrolled_vertices_from_axial(axial_coords, size, offset):
	center = get_center_coords(axial_coords, size)
	center = add_coords(center, offset)
	vertices = unroll_coords(get_vertices(center, size))
	return vertices

def get_center_coords(axial_coords, size):
	center_x = size * math.sqrt(3) * (axial_coords[0] + axial_coords[1] * 0.5)
	center_y = size * 1.5 * axial_coords[1]
	return (center_x, center_y)

def get_vertices(center, size):
	pos_x_diff = size * math.sqrt(3) * 0.5
	pos_y_diff = size * 0.5

	return (
				add_coords(center, (0, size)),
				add_coords(center, (pos_x_diff, pos_y_diff)),
				add_coords(center, (pos_x_diff, -pos_y_diff)),
				add_coords(center, (0, -size)),
				add_coords(center, (-pos_x_diff, -pos_y_diff)),
				add_coords(center, (-pos_x_diff, pos_y_diff))
		   )

def unroll_coords(coords):
	ret = []
	for coord in coords:
		ret.append(coord[0])
		ret.append(coord[1])
	return ret

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
	def getValidMoves(self):
		valid_moves = set()
		#if the piece moving would disconnect the hive or the queen is under another piece, it cannot move
		if self.height != len(board[self.coords]) or not is_board_connected_except_coords(self.coords):
			return valid_moves 
		#loop through all six surrounding hexes
		for main_dir_idx in range(len(dirs)):
			off_dir_idx1 = (main_dir_idx + 1) % 6
			off_dir_idx2 = (main_dir_idx - 1) % 6
			
			main_dir_coords = add_coords(self.coords, dirs[main_dir_idx])
			off_dir_coords1 = add_coords(self.coords, dirs[off_dir_idx1])
			off_dir_coords2 = add_coords(self.coords, dirs[off_dir_idx2])

			#every piece must move by essentially rotating around another piece
			#but a piece cannot fit through a small gap where the points of two other hexes meet
			#thus, to determine if a piece can move to a new hex, we need to look at the two hexes bordering
			#the current location and the desired move location. The movement is valid if one and ONLY one of the
			#"other" two hexes is occupied
			if main_dir_coords not in board and ((off_dir_coords1 in board and off_dir_coords1 != self.coords) != (off_dir_coords2 in board and off_dir_coords1 != self.coords)):
				valid_moves.add(main_dir_coords)
		return valid_moves

class Ant(Bug):
	def getValidMoves(self):
		valid_moves = set()
		#if the piece moving would disconnect the hive or the queen is under another piece, it cannot move
		if self.height != len(board[self.coords]) or not is_board_connected_except_coords(self.coords):
			return valid_moves 
		stack = [self.coords]
		while stack:
			cur_coords = stack.pop()
			if cur_coords not in valid_moves:
				valid_moves.add(cur_coords)
				for main_dir_idx in range(len(dirs)):
					off_dir_idx1 = (main_dir_idx + 1) % 6
					off_dir_idx2 = (main_dir_idx - 1) % 6
					
					main_dir_coords = add_coords(cur_coords, dirs[main_dir_idx])
					off_dir_coords1 = add_coords(cur_coords, dirs[off_dir_idx1])
					off_dir_coords2 = add_coords(cur_coords, dirs[off_dir_idx2])

					#every piece must move by essentially rotating around another piece
					#but a piece cannot fit through a small gap where the points of two other hexes meet
					#thus, to determine if a piece can move to a new hex, we need to look at the two hexes bordering
					#the current location and the desired move location. The movement is valid if one and ONLY one of the
					#"other" two hexes is occupied
					if main_dir_coords not in board and ((off_dir_coords1 in board and off_dir_coords1 != self.coords) != (off_dir_coords2 in board and off_dir_coords2 != self.coords)) and main_dir_coords not in valid_moves:
						stack.append(main_dir_coords)
		valid_moves.remove(self.coords)
		return valid_moves

# board[(0,0)] = [Queen((0,0), 'w')]
# board[(1,0)] = [Queen((1,0), 'b')]
# board[(1,1)] = [Queen((1,1), 'w')]

def test_ant_movement():
	global board
	#first test
	non_ant_hexes = [(0,-2),
	(-1,-1), (0,-1), (1,-1),
	(-1,0), (1,0),
	(0,1), (1,1)]

	board = {x:0 for x in non_ant_hexes}
	board[(0,2)] = [Ant((0,2), 'w')]

	print( "Test 1: ", board[(0,2)][-1].getValidMoves() ==
		set([(0,-3), (1,-3),
			(-1,-2), (1,-2), (2,-2),
			(-2,-1), (2,-1),
			(-2,0), (2,0),
			(-2,1), (-1,1), (2,1),
			(-1,2), (1,2)])
		)

	display_board(50, selected_hex=(0,2), valid_moves=board[(0,2)][-1].getValidMoves())

	#second test
	non_ant_hexes = [(1,-2), (2,-2), (3,-2),
	(1,-1),
	(-1,0), (0,0), (1,0), (2,0)]

	board = {x:0 for x in non_ant_hexes}
	board[(0,-2)] = [Ant((0,-2), 'w')]

	print( "Test 2: ", board[(0,-2)][-1].getValidMoves() ==
		set([(1,-3), (2,-3), (3,-3), (4,-3),
			(4,-2),
			(-1,-1), (0,-1), (3,-1),
			(-2,0), (3,0),
			(-2,1), (-1,1), (0,1), (1,1), (2,1)])
		)

def test_queen_movement():
	global board
	non_queen_hexes = [(0,-2),
	(-1,-1), (0,-1), (1,-1),
	(-1,0), (1,0),
	(0,1), (1,1)]

	board = {x:0 for x in non_queen_hexes}
	board[(0,2)] = [Queen((0,2), 'w')]

	print( board[(0,2)][-1].getValidMoves() )

	display_board(50, selected_hex=(0,2), valid_moves=board[(0,2)][-1].getValidMoves())

test_queen_movement()
test_ant_movement()