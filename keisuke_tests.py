from keisuke import *
from propagators import *
import sys


def run_puzzle(n):
    p = create_keisuke_puzzle(n)
    csp,var_array = keisuke_csp_model_1(p[0], p[1], p[2])

    solver = BT(csp)
    print("GAC")
    solver.bt_search(prop_GAC)
    print("Solution")
    print_sudo_soln(var_array)
    print("===========")


def run_hard_puzzle(n, m):
    p = create_keisuke_puzzle_hard(n, m)
    csp,var_array = keisuke_csp_model_1(p[0], p[1], p[2])

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