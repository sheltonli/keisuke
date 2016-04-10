import unittest
from propagators import *
from keisuke import *
from random import shuffle


class TestKeisukePuzzles(unittest.TestCase):

    def test_regular_puzzle(self):
        game_board = [[0,0,-1,0,0], [-1,0,0,0,0], [0,0,0,-1,0], [0,0,0,0,0], [-1,0,-1,0,-1]]
        horizontal = [(2,3), (1,3), (3,2,2,1), (2,3,3), (2,1,2,2,2)]
        vertical = [(2,2), (3,3,3,1,3), (2,3,2), (1,2), (2,1), (3,1,3,2)]

        csp,var_array = keisuke_csp(game_board, horizontal, vertical)
        solver = BT(csp)
        solver.bt_search(prop_GAC)

        result = []
        for i in range(5):
            for j in range(5):
                result.append(var_array[i][j].cur_domain())

        answer = [[2], [3], [-1], [1], [3], [-1], [3], [2], [2], [1], [2], [3], [3], [-1], [3], [2], [1], [2], [2], [2], [-1], [3], [-1], [1], [-1]]
        self.assertEqual(answer, result)

    def test_regular_puzzle_numeric_shuffled(self):
        game_board = [[0,0,-1,0,0], [-1,0,0,0,0], [0,0,0,-1,0], [0,0,0,0,0], [-1,0,-1,0,-1]]
        horizontal = [(2,3), (1,3), (3,2,2,1), (2,3,3), (2,1,2,2,2)]
        vertical = [(2,2), (3,3,3,1,3), (2,3,2), (1,2), (2,1), (3,1,3,2)]

        shuffle(horizontal)
        shuffle(vertical)

        csp,var_array = keisuke_csp(game_board, horizontal, vertical)
        solver = BT(csp)
        solver.bt_search(prop_GAC)

        result = []
        for i in range(5):
            for j in range(5):
                result.append(var_array[i][j].cur_domain())

        answer = [[2], [3], [-1], [1], [3], [-1], [3], [2], [2], [1], [2], [3], [3], [-1], [3], [2], [1], [2], [2], [2], [-1], [3], [-1], [1], [-1]]
        self.assertEqual(answer, result)

    def test_hard_puzzle(self):
        game_board = [[0, 0, -1, 0, 0], [0, 0, -1, 0, 0], [-1, -1, -1, -1, -1], [0, 0, -1, 0, 0], [0, 0, -1, 0, 0]]
        horizontal = [(7, 5), (8, 9), (1, 9), (5, 5), (7, 5), (7, 1), (5, 5), (9, 2)]
        vertical = [(7, 1), (7, 5), (5, 9), (5, 5), (8, 5), (7, 9), (9, 5), (1, 2)]

        csp,var_array = keisuke_csp(game_board, horizontal, vertical)
        solver = BT(csp)
        solver.bt_search(prop_GAC)

        result = []
        for i in range(5):
            for j in range(5):
                result.append(var_array[i][j].cur_domain())

        answer = [[7], [1], [-1], [7], [5], [9], [2], [-1], [1], [9], [-1], [-1], [-1], [-1], [-1], [7], [5], [-1], [8], [9], [5], [5], [-1], [5], [5]]
        self.assertEqual(answer, result)


if __name__ == "__main__":
    unittest.main()