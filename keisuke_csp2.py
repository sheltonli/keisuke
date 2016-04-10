from cspbase import *
from keisuke import *
import itertools

def isplit(iterable, splitters):
    return [int("".join([str(e) for e in list(g)])) for k,g in itertools.groupby(iterable,lambda x:x in splitters) if not k]

def get_section_coord(row_or_col):
	ls_coord = []
	start = False
	for i in range(len(row_or_col)):
		cell = row_or_col[i]
		if cell!=-1 and not start:
			ls_coord.append(i)
		if cell!=-1:
			start = True
		if cell==-1:
			start = False
	return ls_coord

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

	ls_hr_section = isplit(board_row, (-1,))
	ls_vr_section = isplit(board_col, (-1,))
	ls_x = get_section_coord(board_row)
	ls_y = get_section_coord(board_col)
	# make variables by row	
	n = 0

	for i in range(len(ls_hr_section)):
		section = ls_hr_section[i]
		if len(str(section)) > 1:
			var = Variable("H({},{})".format(ls_x[i], y), [val for val in horizontal if len(str(val))==len(str(section))])			
			ls_var.append(var)

	# make variables by columns	
	for i in range(len(ls_vr_section)):
		section = ls_vr_section[i]
		if len(str(section)) > 1:
			var = Variable("V({},{})".format(y, ls_y[i]), [val for val in vertical if len(str(val))==len(str(section))])
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
		var_ls, n_var = make_variables(initial_keisuke_board, y, n, horizontal, vertical)
		n += n_var
		var_ls_ls.append(var_ls)

	return var_ls_ls

def get_all_coord(var):
	v_length = len(str(var.domain()[0]))
	x = int(var.name[var.name.index("(")+1:var.name.index(",")])
	y = int(var.name[var.name.index(",")+1:var.name.index(")")])
	if var.name[0]=="H":
		return [(x+i,y) for i in range(v_length)]
	else:
		return [(x,y+i) for i in range(v_length)]


def find_intersect(v1, v2):
	# print("is {} intersect {}?".format(v1.name, v2.name))
	ls_v1_coords = get_all_coord(v1)
	ls_v2_coords = get_all_coord(v2)

	for coord1 in ls_v1_coords:
		for coord2 in ls_v2_coords:
			if coord1==coord2:
				return coord1
	return None

def add_bin_intersection_constraints(csp, ls_var):
	ls_varpairs = [pair for pair in itertools.combinations(ls_var, 2)]
	print("\nget interseting pairs\n")
	ls_intersect_pairs = [(pair, find_intersect(pair[0], pair[1]))\
						 for pair in ls_varpairs if find_intersect(pair[0], pair[1]) != None]

	for pair in ls_intersect_pairs:
		print(pair, pair[0][1].cur_domain(), pair[0][1].cur_domain())

	i = 0
	for p in ls_intersect_pairs:
		pair, coord = p
		v1 = pair[0]
		v2 = pair[1]
		coord1 = [c for c in get_all_coord(v1) if c == coord][0]
		coord2 = [c for c in get_all_coord(v2) if c == coord][0]

		cons = Constraint("int-{}".format(i), [v1, v2])
		sat_tuples = []

		for val1 in v1.cur_domain():
			for val2 in v2.cur_domain():
				# coord is (x, y)
				# print("coord: ", coord)
				# print("coord1: ", coord1, "diff: ", abs(coord[0]-coord1[0])+abs(coord[1]-coord1[1]))
				# print("coord2: ", coord2, "diff: ", abs(coord[0]-coord2[0])+abs(coord[1]-coord2[1]))
				value1 = int(str(val1)[abs(coord[0]-coord1[0])+abs(coord[1]-coord1[1])])
				value2 = int(str(val2)[abs(coord[0]-coord2[0])+abs(coord[1]-coord2[1])])
				if value1==value2:
					# print("{}:{} x {}:{}".format(v1.name, v1.cur_domain(), v2.name, v2.cur_domain()))
					# print("{}: {}=={}".format(coord, value1, value2))
					# print("sat_tuple: ", (val1, val2))
					sat_tuples.append((val1, val2))
				# else:
				# 	print("{}:{} x {}:{}".format(v1.name, v1.cur_domain(), v2.name, v2.cur_domain()))
				# 	print("{}: {}!={}".format(coord, value1, value2))
				# 	print("sat_tuple: ", (val1, val2))
					# assert(False)
				# sat_tuples.append((val1, val2))
		# assert(len(sat_tuples)!=0)
		cons.add_satisfying_tuples(sat_tuples)
		csp.add_constraint(cons)
		i += 1

def add_bin_constraint(csp, board, ls_var, horizontal, vertical):
	board_size = len(board)	
	map_hr_cons = {len(str(var.cur_domain()[0])): [] for var in ls_var}
	map_vr_cons = {len(str(var.cur_domain()[0])): [] for var in ls_var}

	horizontal = [int("".join([str(n) for n in tup])) for tup in horizontal]
	vertical = [int("".join([str(n) for n in tup])) for tup in vertical]

	for var in ls_var:
		if var.name[0]=="H":
			var_length = len(str(var.cur_domain()[0]))
			map_hr_cons[var_length].append(var)
		else:
			var_length = len(str(var.cur_domain()[0]))
			map_vr_cons[var_length].append(var)

	# horizontal constraints
	for length in map_hr_cons:
		scope = map_hr_cons[length]
		if scope!=[]:
			cons = Constraint("H{}".format(length), scope)
			
			# add sat_tuples
			ls_tuples = [tup for tup in horizontal if len(str(tup))==length]
			all_tuples = [c for c in itertools.permutations(ls_tuples, 2)]		
			# if all_tuples==[]:
			# 	all_tuples = [(scope[0].cur_domain(),)]
			cons.add_satisfying_tuples(all_tuples)
			csp.add_constraint(cons)		

			print(cons)
			print(all_tuples)
		# if all_tuples==[]:
		# 	print("\t", scope[0].cur_domain())

	# vertical constraints
	for length in map_vr_cons:
		scope = map_vr_cons[length]
		if scope!=[]:
			cons = Constraint("V{}".format(length), scope)

			# add sat_tuples
			ls_tuples = [tup for tup in vertical if len(str(tup))==length]
			all_tuples = [c for c in itertools.permutations(ls_tuples, 2)]
			# if all_tuples==[]:
			# 	all_tuples = [(scope[0].cur_domain(),)]

			print(cons)
			print(all_tuples)

			cons.add_satisfying_tuples(all_tuples)
			csp.add_constraint(cons)

if __name__=="__main__":

	keisuke_board, horizontal, vertical = create_keisuke_puzzle_3(5)

	print("board:")
	for row in keisuke_board:
		print(row)
	print("horizontal:", horizontal)
	print("vertical: ", vertical)

	# for ls_var in create_var_ls_ls(keisuke_board, horizontal , vertical):
	# 	for var in ls_var:
	# 		var.print_all()

	ls_ls_var = create_var_ls_ls(keisuke_board, horizontal , vertical)
	ls_var = []
	for lsv in ls_ls_var:
		for var in lsv:
			ls_var.append(var)
	# for var in ls_var:
	# 	print(var)
	# print("\npairs\n")
	# for pair in itertools.combinations(ls_var, 2):
	# 	print(pair)

	csp = CSP("Version-2", ls_var)	
	# add_bin_intersection_constraints(csp, ls_var)
	add_bin_constraint(csp, keisuke_board, ls_var, horizontal, vertical)

	solver = BT(csp)
	print("BT")
	solver.bt_search(prop_BT)
	for var in ls_var:
		# print(var)
		print("assignedval: ", var.get_assigned_value())

	csp.print_soln()

	ls_cons = csp.get_all_cons()
	# for cons in ls_cons:
	# 	print(cons.name)
	# 	print(cons.get_scope())
	# 	for var in cons.get_scope():
	# 		var.print_all()
	# 	for sat_tuple in cons.sat_tuples.keys():
	# 		print(sat_tuple)
	# 	print("")
	# print("Solution")
	# print_sudo_soln(ls_var)
	# print("===========")

	# for c in itertools.combinations(ls_var, 2):
	# 	print(c)