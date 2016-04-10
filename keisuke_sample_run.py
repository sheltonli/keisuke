from keisuke import *
from propagators import *
from random import choice
import sys


def create_keisuke_puzzle(n):
    '''
    Creates a randomly valid keisuke puzzle that is of dimension n x n.
    Will return a list representation of the puzzle along with a horizontal and vertical list of numeric values.
    '''

    possible_values = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    game_board = [[choice(possible_values) for x in range (n)] for y in range(n)]

    horizontal = []
    vertical = []

    for row in game_board:
        temp = ()
        for item in row:
            if item == -1:
                if temp != () and len(temp) > 1:
                    horizontal.append(temp)
                temp = ()
            else:
                temp += (item,)
        if temp != () and len(temp) > 1:
            horizontal.append(temp)

    for i in range(n):
        temp = ()
        for row in game_board:
            if row[i] == -1:
                if temp != () and len(temp) > 1:
                    vertical.append(temp)
                temp = ()
            else:
                temp += (row[i],)
        if temp != () and len(temp) > 1:
            vertical.append(temp)

    final_board = [[item if item == -1 else 0 for item in row] for row in game_board]

    return final_board, horizontal, vertical


def create_keisuke_puzzle_hard(n, m):
    '''
    Creates a more difficult version of a Keisuke puzzle.
    Similar to create_keisuke_puzzle, this function creates a puzzle of size n but tries to maximize the number
    of subsections of size m. It does this by placing a blacked out cell after each subsection of size m. A blacked out
    cell is placed both horizontally and vertically.

    For an example, given n = 5, and m = 2, it will create a 5 by 5 board with blacked out cells filling the third
    column and the third row.

    This function will return a list representation of the puzzle along with a horizontal and vertical list of numeric
    values.
    '''

    possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    game_board = []
    for i in range(1,n+1):
        game_board.append([])
        for j in range(1,n+1):
            if i % (m+1) == 0 or j % (m+1) == 0:
                game_board[i-1].append(-1)
            else:
                game_board[i-1].append(choice(possible_values))
    horizontal = []
    vertical = []

    for row in game_board:
        temp = ()
        for item in row:
            if item == -1:
                if temp != () and len(temp) > 1:
                    horizontal.append(temp)
                temp = ()
            else:
                temp += (item,)
        if temp != () and len(temp) > 1:
            horizontal.append(temp)

    for i in range(n):
        temp = ()
        for row in game_board:
            if row[i] == -1:
                if temp != () and len(temp) > 1:
                    vertical.append(temp)
                temp = ()
            else:
                temp += (row[i],)
        if temp != () and len(temp) > 1:
            vertical.append(temp)

    final_board = [[item if item == -1 else 0 for item in row] for row in game_board]

    return final_board, horizontal, vertical


def print_sudo_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])


def print_sudo(var_array):
    for row in var_array:
        print([var for var in row])


def run_puzzle(n):
    p = create_keisuke_puzzle(n)
    game_board = p[0]
    horizontal = p[1]
    vertical = p[2]

    print("Puzzle")    
    print_sudo(game_board)
    print("ACROSS")
    print_sudo(horizontal)
    print("DOWN")
    print_sudo(vertical)    
    print("")
    
    csp,var_array = keisuke_csp(game_board, horizontal, vertical)

    solver = BT(csp)
    print("GAC")
    solver.bt_search(prop_GAC)
    print("Solution")
    print_sudo_soln(var_array)
    print("===========")


def run_hard_puzzle(n, m):
    p = create_keisuke_puzzle_hard(n, m)
    game_board = p[0]
    horizontal = p[1]
    vertical = p[2]

    print("Puzzle")    
    print_sudo(game_board)
    print("ACROSS")
    print_sudo(horizontal)
    print("DOWN")
    print_sudo(vertical)    
    print("")
    
    csp,var_array = keisuke_csp(game_board, horizontal, vertical)

    solver = BT(csp)
    print("GAC")
    solver.bt_search(prop_GAC)
    print("Solution")
    print_sudo_soln(var_array)
    print("===========")

if __name__ == '__main__':
    sys.setrecursionlimit(3000)
    run_puzzle(5)
    # run_hard_puzzle(5, 2)