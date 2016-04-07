from keisuke import *


if __name__ == '__main__':
    csp,var_array = keisuke_csp_model_1(p[0], p[1], p[2])


    solver = BT(csp)
    print("GAC")
    solver.bt_search(prop_GAC)
    print("Solution")
    # print_sudo_soln(var_array)
    # print("===========")