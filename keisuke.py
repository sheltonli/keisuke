from random import choice, random
from cspbase import *


def keisuke_csp(initial_keisuke_board, horizontal, vertical):
    '''
    Return a CSP object that represents keisuke and an array of variables.
    Each variable represents a cell in the puzzle.
    There are two types of constraints.
    The first is the size and orientation constraint. The satisfying values for
    this constraint is the numeric values that match the size and orientation of
    the subsection.
    The second type of constraint is similar to the binary alldifferent constraint.
    These will be constraints between all combinations of two subsections that
    have the same size and orientation to ensure that every numeric value
    is used for only one subsection.
    '''
    csp = CSP("Keiuske_M1")
    n = len(initial_keisuke_board)
    variables = []
    
    # separate constraints by length
    horizontal_by_length = [[] for i in range(n+1)];
    for i in range(len(horizontal)):
        horizontal_by_length[len(horizontal[i])].append(horizontal[i])
    
    vertical_by_length = [[] for i in range(n+1)];
    for i in range(len(vertical)):
        vertical_by_length[len(vertical[i])].append(vertical[i])
    
    
    # create domain
    domain = set()
    for i in range(len(horizontal)):
        domain = domain.union(set(horizontal[i]))
    for i in range(len(vertical)):
        domain = domain.union(set(vertical[i]))

    # create variables
    for i in range(n):
        variables.append([])
        for j in range(n):
            var = Variable("V{},{}".format(i,j))
            if initial_keisuke_board[i][j] == 0:
                var.add_domain_values(domain)
            else:
                var.add_domain_values([-1])
            variables[i].append(var)
            csp.add_var(var)
                
                
    ############### create constraints #############
    
    row_constraints = [] 
    column_constraints = []
    
    # create row constraints
    for i in range(n):
        first_white_slot = 0
        for j in range(n):
            if (j == 0 and initial_keisuke_board[i][j] == -1):
                first_white_slot = 1
            if ((j == n-1 and initial_keisuke_board[i][j] != -1)
            or (j != n-1 and initial_keisuke_board[i][j+1] == -1)):
                length = j - first_white_slot + 1
                if length > 1:
                    con = Constraint("H", [variables[i][k] for k in range(first_white_slot, j+1)])
                    con.add_satisfying_tuples(horizontal_by_length[length])
                    csp.add_constraint(con)
                    row_constraints.append(con)
                        
                first_white_slot = j+2


    # create column constraints
    for i in range(n):
        first_white_slot = 0
        for j in range(n):
            if (j == 0 and initial_keisuke_board[j][i] == -1):
                first_white_slot = 1
            if ((j == n-1 and initial_keisuke_board[j][i] != -1)
            or (j != n-1 and initial_keisuke_board[j+1][i] == -1)):
                length = j - first_white_slot + 1
                if length > 1:
                    con = Constraint("C", [variables[k][i] for k in range(first_white_slot, j+1)])
                    con.add_satisfying_tuples(vertical_by_length[length])
                    csp.add_constraint(con)
                    column_constraints.append(con)
                        
                first_white_slot = j+2

    # create alldiff constraints
    # separate constraints by length
    row_cons_length = [[] for i in range(n+1)]
    for i in range(len(row_constraints)):
        row_cons_length[len(row_constraints[i].get_scope())].append(row_constraints[i])
        
    column_cons_length = [[] for i in range(n+1)]
    for i in range(len(column_constraints)):
        column_cons_length[len(column_constraints[i].get_scope())].append(column_constraints[i])   
        
    
    # create binary difference between two same length horizontal subsections
    for i in range(2, len(row_cons_length)):
        same_length_cons = row_cons_length[i]
        
        for j in range(len(same_length_cons)):
            for k in range(j+1, len(same_length_cons)):
                con = Constraint("H-diff",
                                 same_length_cons[j].get_scope() + same_length_cons[k].get_scope())
                
                # create a list of satisfiable tuples
                sat_tuple = []
                for l in range(len(horizontal_by_length[i])):
                    for m in range(len(horizontal_by_length[i])):
                        if (l != m):
                            sat_tuple.append(horizontal_by_length[i][l] + horizontal_by_length[i][m])

                con.add_satisfying_tuples(sat_tuple)
                csp.add_constraint(con)
        
    # create binary difference between two same length vertical subsections
    for i in range(2, len(column_cons_length)):
        same_length_cons = column_cons_length[i]
        
        for j in range(len(same_length_cons)):
            for k in range(j+1, len(same_length_cons)):
                con = Constraint("V-diff",
                                 same_length_cons[j].get_scope() + same_length_cons[k].get_scope())
                
                # create a list of satisfiable tuples
                sat_tuple = []
                for l in range(len(vertical_by_length[i])):
                    for m in range(len(vertical_by_length[i])):
                        if (l != m):
                            sat_tuple.append(vertical_by_length[i][l] + vertical_by_length[i][m])

                con.add_satisfying_tuples(sat_tuple)
                csp.add_constraint(con)
                
    return (csp, variables)
                  


