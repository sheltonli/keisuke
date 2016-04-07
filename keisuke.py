from random import choice, random


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

    print(game_board)
    print(final_board)
    print(horizontal)
    print(vertical)
    return final_board, horizontal, vertical


def create_keisuke_puzzle_2(n):
    '''
    Creates a randomly valid keisuke puzzle that is of dimension n x n.
    Will return a list representation of the puzzle along with the list of numeric values.

    Possible version where we adjust the occurrence of black squares.
    '''

    quarter = n / 4
    percent = quarter / n
    possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    game_board = [[choice(possible_values) if random() >= percent else -1 for x in range (n)] for y in range(n)]

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

if __name__ == '__main__':
    create_keisuke_puzzle(5)
