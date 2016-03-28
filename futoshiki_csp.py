#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

'''
Construct and return Futoshiki CSP models.
'''

from cspbase import *
import itertools

def futoshiki_csp_model_1(initial_futoshiki_board):
    '''Return a CSP object representing a Futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, variable_array

    where futoshiki_csp is a csp representing futoshiki using model_1 and
    variable_array is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to
    represent the value to be placed in cell i,j of the futoshiki board
    (indexed from (0,0) to (n-1,n-1))


    The input board is specified as a list of n lists. Each of the n lists
    represents a row of the board. If a 0 is in the list it represents an empty
    cell. Otherwise if a number between 1--n is in the list then this
    represents a pre-set board position.

    Each list is of length 2n-1, with each space on the board being separated
    by the potential inequality constraints. '>' denotes that the previous
    space must be bigger than the next space; '<' denotes that the previous
    space must be smaller than the next; '.' denotes that there is no
    inequality constraint.

    E.g., the board

    -------------------
    | > |2| |9| | |6| |
    | |4| | | |1| | |8|
    | |7| <4|2| | | |3|
    |5| | | | | |3| | |
    | | |1| |6| |5| | |
    | | <3| | | | | |6|
    |1| | | |5|7| |4| |
    |6> | |9| < | |2| |
    | |2| | |8| <1| | |
    -------------------
    would be represented by the list of lists

    [[0,'>',0,'.',2,'.',0,'.',9,'.',0,'.',0,'.',6,'.',0],
     [0,'.',4,'.',0,'.',0,'.',0,'.',1,'.',0,'.',0,'.',8],
     [0,'.',7,'.',0,'<',4,'.',2,'.',0,'.',0,'.',0,'.',3],
     [5,'.',0,'.',0,'.',0,'.',0,'.',0,'.',3,'.',0,'.',0],
     [0,'.',0,'.',1,'.',0,'.',6,'.',0,'.',5,'.',0,'.',0],
     [0,'.',0,'<',3,'.',0,'.',0,'.',0,'.',0,'.',0,'.',6],
     [1,'.',0,'.',0,'.',0,'.',5,'.',7,'.',0,'.',4,'.',0],
     [6,'>',0,'.',0,'.',9,'.',0,'<',0,'.',0,'.',2,'.',0],
     [0,'.',2,'.',0,'.',0,'.',8,'.',0,'<',1,'.',0,'.',0]]


    This routine returns Model_1 which consists of a variable for each cell of
    the board, with domain equal to [1,...,n] if the board has a 0 at that
    position, and domain equal [i] if the board has a fixed number i at that
    cell.

    Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between all relevant
    variables (e.g., all pairs of variables in the same row, etc.).

    All of the constraints of Model_1 MUST BE binary constraints (i.e.,
    constraints whose scope includes two and only two variables).
    '''
    csp = CSP("Futoshiki-M1")
    n = len(initial_futoshiki_board)
    variables = []
    # create variables
    for i in range(n):
        variables.append([])
        for j in range(2*n-1):
            if (j % 2) == 0:
                var = Variable("V{},{}".format(i,int(j/2)))
                if initial_futoshiki_board[i][j] == 0:
                    var.add_domain_values([i+1 for i in range(n)])
                else:
                    var.add_domain_values([initial_futoshiki_board[i][j]])
                variables[i].append(var)
                csp.add_var(var)
                
                # ineq constraint
                if (not j == 0) and (not initial_futoshiki_board[i][j-1] == '.'):
                    var1 = variables[i][int(j/2)-1]
                    var2 = variables[i][int(j/2)]
                    con = Constraint(
                        "C{},{}{}{}".format(i,int(j/2)-1,initial_futoshiki_board[i][j-1],int(j/2)),
                    [var1, var2])
                    sat_tuples = []
                    
                    for val1 in var1.cur_domain():
                        for val2 in var2.cur_domain():
                            if ((initial_futoshiki_board[i][j-1] == '>' and val1 > val2)
                                or (initial_futoshiki_board[i][j-1] == '<' and val1 < val2)):
                                sat_tuples.append((val1, val2))
                    con.add_satisfying_tuples(sat_tuples)
                    csp.add_constraint(con)
    
    # create row constraints
    for i in range(n): #each row
        for j in range(n):
            var1 = variables[i][j]
            for k in range(j+1, n):
                var2 = variables[i][k]
                con = Constraint("C{},{}!={}".format(i,j,k), [var1, var2])
                sat_tuples = []
                for val1 in var1.cur_domain():
                    for val2 in var2.cur_domain():
                        if not val1 == val2:
                            sat_tuples.append((val1, val2))
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)
    
    # create column constraints
    for j in range(n): #each col
        for i in range(n):
            var1 = variables[i][j]
            for k in range(i+1, n):
                var2 = variables[k][j]
                con = Constraint("C{}!={},{}".format(i,k,j), [var1, var2])
                sat_tuples = []
                for val1 in var1.cur_domain():
                    for val2 in var2.cur_domain():
                        if not val1 == val2:
                            sat_tuples.append((val1, val2))
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)
    return (csp, variables)
#IMPLEMENT

##############################

def futoshiki_csp_model_2(initial_futoshiki_board):
    '''Return a CSP object representing a futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, variable_array

    where futoshiki_csp is a csp representing futoshiki using model_2 and
    variable_array is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to
    represent the value to be placed in cell i,j of the futoshiki board
    (indexed from (0,0) to (n-1,n-1))

    The input board takes the same input format (a list of n lists of size 2n-1
    specifying the board) as futoshiki_csp_model_1.

    The variables of Model_2 are the same as for Model_1: a variable for each
    cell of the board, with domain equal to [1,...,n] if the board has a 0 at
    that position, and domain equal [n] if the board has a fixed number i at
    that cell.

    However, Model_2 has different constraints. In particular, instead of
    binary non-equals constaints Model_2 has 2*n all-different constraints:
    all-different constraints for the variables in each of the n rows, and n
    columns. Each of these constraints is over n-variables (some of these
    variables will have a single value in their domain). Model_2 should create
    these all-different constraints between the relevant variables, and then
    separately generate the appropriate binary inequality constraints as
    required by the board. There should be j of these constraints, where j is
    the number of inequality symbols found on the board.  
    '''
    csp = CSP("Futoshiki-M2")
    n = len(initial_futoshiki_board)
    variables = []
    # create variables
    for i in range(n):
        variables.append([])
        for j in range(2*n-1):
            if (j % 2) == 0:
                var = Variable("V{},{}".format(i,int(j/2)))
                if initial_futoshiki_board[i][j] == 0:
                    var.add_domain_values([i+1 for i in range(n)])
                else:
                    var.add_domain_values([initial_futoshiki_board[i][j]])
                variables[i].append(var)
                csp.add_var(var)
                
                # ineq constraint
                if (not j == 0) and (not initial_futoshiki_board[i][j-1] == '.'):
                    var1 = variables[i][int(j/2)-1]
                    var2 = variables[i][int(j/2)]
                    con = Constraint(
                        "C{},{}{}{}".format(i,int(j/2)-1,initial_futoshiki_board[i][j-1],int(j/2)),
                    [var1, var2])
                    sat_tuples = []
                    
                    for val1 in var1.cur_domain():
                        for val2 in var2.cur_domain():
                            if ((initial_futoshiki_board[i][j-1] == '>' and val1 > val2)
                                or (initial_futoshiki_board[i][j-1] == '<' and val1 < val2)):
                                sat_tuples.append((val1, val2))
                    con.add_satisfying_tuples(sat_tuples)
                    csp.add_constraint(con)

    # create row constraints
    for i in range(n): #each row
        sat_tuples = []
        helper_rec(0, n, [], variables[i], sat_tuples)
        con = Constraint("Crow{}".format(i), variables[i])
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)
    
    # create row constraints
    for j in range(n):
        sat_tuples = []
        var_col = [variables[i][j] for i in range(n)]
        helper_rec(0, n, [], var_col, sat_tuples)
        con = Constraint("Ccol{}".format(j), var_col)
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)
    return (csp, variables)

#IMPLEMENT

def helper_rec(level, n, lst, varS, acc):
    if level == n:
        acc = acc.append(tuple(lst))
    else:
        for val in varS[level].cur_domain():
            new_lst = list(lst)
            new_lst.append(val)
            if len(set(new_lst)) == level+1:
                helper_rec(level+1, n, new_lst, varS, acc)