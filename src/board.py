from collections import defaultdict
from texttable import Texttable

class Board:
    def __init__(self, size):
        self.__size = size
        self.__board = [[' ' for _ in range(self.__size)] for _ in range(self.__size)]
        self.__moves = []
        self.__obstructions = defaultdict(list)  # Tracks obstructed squares for each move

    @property
    def size(self):
        return self.__size

    def get_board(self):
        return self.__board

    def update_position(self, row, column, symbol):
        if not 0 < row <= self.__size or not 0 < column <= self.__size:
            raise ValueError("Invalid position on board.")

        if self.__board[row - 1][column - 1] != ' ':
            raise ValueError(f"The space {row}, {column} has already been played.")

        self.__board[row - 1][column - 1] = symbol  # update the board with the symbol 'X' or 'O'
        self.__moves.append((row, column, symbol))  # add the move to the list of moves

        # Obstruct squares in the 3×3 area
        for i in range(row - 2, row + 1):
            for j in range(column - 2, column + 1):
                if 0 <= i < self.__size and 0 <= j < self.__size and self.__board[i][j] == ' ':
                    self.__board[i][j] = '/'
                    self.__obstructions[(row, column)].append((i, j))  # Track this obstruction

    def reset_position(self, row, column):
        if not 0 < row <= self.__size or not 0 < column <= self.__size:
            raise ValueError("Invalid position on board.")

        if (row, column) not in [(move[0], move[1]) for move in self.__moves]:
            raise ValueError("Position not found in moves.")

        # Remove the move
        self.__moves = [move for move in self.__moves if (move[0], move[1]) != (row, column)]
        self.__board[row - 1][column - 1] = ' '  # Clear the position

        # Clear only the obstructions caused by this move
        for i, j in self.__obstructions[(row, column)]:
            if self.__board[i][j] == '/':  # Clear obstruction if it’s still obstructed
                self.__board[i][j] = ' '
        del self.__obstructions[(row, column)]  # Remove obstruction tracking for this move

    def is_full(self):
        for row in self.__board:
            if ' ' in row:
                return False
        return True

    def is_empty(self, row, column):
        return self.__board[row - 1][column - 1] == ' '

    def get_board_status(self) -> str:
        if self.is_full():
            if self.__moves and self.__moves[-1][2] == 'X':
                return "human"
            else:
                return "computer"
        return "playing"

    def __str__(self):
        table = Texttable()
        header = ['/']
        for i in range(self.__size):
            header.append(i + 1)
        table.add_row(header)

        i = 1
        for row in self.__board:
            row = [elem for elem in row]
            table.add_row([i] + row)
            i += 1
        return table.draw()
