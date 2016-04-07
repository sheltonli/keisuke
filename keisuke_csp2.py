from cspbase import *
from keisuke import *
import itertools

def isplit(iterable, splitters):
    return [int("".join([str(e) for e in list(g)])) for k,g in itertools.groupby(iterable,lambda x:x in splitters) if not k]

def make_variables(board, y, n, horizontal, vertical):
	"""
	change the every tuple in horizontal and vertical in int 
	for easy handle
	[(9,1), (1,2)] => [91,12]

	make list of vars"""
	board_row = board[y]
	board_col = [row[y] for row in board]
	horizontal = [int("".join([str(n) for n in tup])) for tup in horizontal]
	vertical = [int("".join([str(n) for n in tup])) for tup in vertical]
	ls_var = []	

	# make variables by row
	ls_section = isplit(board_row, (-1,))
	for i in range(len(ls_section)):		
		section = ls_section[i]
		if len(str(section)) > 1:
			var = Variable("H-{}".format(n+i), [val for val in horizontal if len(str(val))==len(str(section))])
			ls_var.append(var)

	# make variables by columns
	ls_section = isplit(board_col, (-1,))
	for i in range(len(ls_section)):		
		section = ls_section[i]
		if len(str(section)) > 1:
			var = Variable("V-{}".format(n+i), [val for val in vertical if len(str(val))==len(str(section))])
			ls_var.append(var)

	return (ls_var, len(ls_var))

def create_var_ls_ls(initial_keisuke_board, horizontal, vertical):
	board_size = len(initial_keisuke_board)
	var_ls_ls = []
	dom = []

	# create domain
	for i in range(board_size):
		dom.append(i+1)

	n = 0
	for y in range(board_size):
		row = initial_keisuke_board[y]
		var_ls = []
		# [0, 2, 4, ... 2n - 1] where n is width of board
		# for x in range(board_size): 
		#   	val = row[x]
		# if val==0:
		#     var = Variable("[{},{}]".format(y,int(x/2)), dom)
		#     var_ls.append(var)
		# else:
		# 	var = Variable("[{},{}]".format(y,int(x/2)), [val])
		# 	var_ls.append(var)

		var_ls, n_var = make_variables(initial_keisuke_board, y, n, horizontal, vertical)
		n += n_var
		var_ls_ls.append(var_ls)

	return var_ls_ls

if __name__=="__main__":

	keisuke_board, horizontal, vertical = create_keisuke_puzzle_3(5)

	print("board:")
	for row in keisuke_board:
		print(row)
	print("horizontal:", horizontal)
	print("vertical: ", vertical)

	for ls_var in create_var_ls_ls(keisuke_board, horizontal , vertical):
		for var in ls_var:
			var.print_all()


	csp = CSP("Version-2", ls_var)