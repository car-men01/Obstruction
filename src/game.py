import math
from random import randint


class ComputerAIMoves:
    def __init__(self):
        pass

    def move(self, board):
        """
        Analyzes the board and performs the best move using minimax with heuristics.
        :param board: The updated board on which the computer plays
        :return: The chosen (row, column)
        """
        best_score = -math.inf
        best_move = None
        depth = 5  # adjust depth for better performance, but greater computation time

        for row in range(1, board.size + 1):
            for column in range(1, board.size + 1):
                if board.is_empty(row, column):
                    board.update_position(row, column, 'O')  # simulate the computer's move
                    score = self.minimax(board, depth - 1, alpha=-math.inf, beta=math.inf, is_maximizing=False)
                    board.reset_position(row, column)  # undo the move

                    if score > best_score:
                        best_score = score
                        best_move = (row, column)

        if best_move:
            board.update_position(best_move[0], best_move[1], 'O')
            return best_move
        return None

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        """
        Minimax algorithm with alpha-beta pruning and heuristic evaluation.
        :param board: The game board
        :param depth: Remaining depth for recursion
        :param alpha: Best value for maximizer so far
        :param beta: Best value for minimizer so far
        :param is_maximizing: True if the current player is the computer, False otherwise
        :return: The calculated score
        """

        board_status = board.get_board_status()
        if board_status == "computer":  # computer wins
            return 100 + depth  # faster wins are better
        elif board_status == "human":  # human wins
            return -100 - depth  # block human wins at all costs
        elif board.is_full() or depth == 0:  # draw or depth limit reached
            return self.evaluate_board(board)  # heuristic evaluation

        if is_maximizing:   # computer's turn
            max_eval = -math.inf
            for row in range(1, board.size + 1):
                for column in range(1, board.size + 1):
                    if board.is_empty(row, column):
                        board.update_position(row, column, 'O')
                        eval_score = self.minimax(board, depth - 1, alpha, beta, False)
                        board.reset_position(row, column)
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:  # prune the remaining branches
                            break
            return max_eval
        else:   # human's turn
            min_eval = math.inf
            for row in range(1, board.size + 1):
                for column in range(1, board.size + 1):
                    if board.is_empty(row, column):
                        board.update_position(row, column, 'X')
                        eval_score = self.minimax(board, depth - 1, alpha, beta, True)
                        board.reset_position(row, column)
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:  # prune the remaining branches
                            break
            return min_eval

    def evaluate_board(self, board):
        """
        Heuristic evaluation of the board.
        :param board: The game board
        :return: A heuristic score
        """
        score = 0

        # Center control: prioritize positions near the center
        center = board.size // 2
        for row in range(1, board.size + 1):
            for column in range(1, board.size + 1):
                if board.get_board()[row - 1][column - 1] == 'O':
                    score += 5 - (abs(center - row) + abs(center - column))  # Closer to center = higher score
                elif board.get_board()[row - 1][column - 1] == 'X':
                    score -= 5 - (abs(center - row) + abs(center - column))  # Penalize human control

        # Block human moves: penalize states where human has potential winning moves
        for row in range(1, board.size + 1):
            for column in range(1, board.size + 1):
                if board.is_empty(row, column):
                    board.update_position(row, column, 'X')  # Simulate human move
                    if board.get_board_status() == "human":
                        score -= 50  # Large penalty for human's winning potential
                    board.reset_position(row, column)

        return score


class ComputerRandomMoves:
    def __init__(self):
        pass

    def move(self, board):
        """
        Generates a random move for the computer
        :param board: The updated board on which the computer plays
        """
        row = randint(1, board.size)
        column = randint(1, board.size)
        valid_move = False
        while not valid_move:
            try:
                board.update_position(row, column, 'O')
                valid_move = True
                return row, column
            except ValueError:
                row = randint(1, board.size)
                column = randint(1, board.size)

class Game:
    def __init__(self, board, computer_player):
        self.__board = board
        self.__computer = computer_player

    def make_user_move(self, row, column, symbol):
        """
        Make the user move on the board
        :param row: chosen row
        :param column: chosen column
        :param symbol: user's symbol 'X'
        """
        self.__board.update_position(row, column, symbol)

    def make_computer_move(self):
        return self.__computer.move(self.__board)
