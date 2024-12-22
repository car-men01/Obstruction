# Obstruction
## Game overview
The game "Obstruction" looks similar to tic-tac-toe, but it's main point is to cover the whole board in 'X', '0' and obstructed squares '/'. The winner is the last player who puts a symbol on the board.
The game can be played using the text-based interface, or the GUI. It has 5 different board sizes available and 2 difficulties: easy and hard, where the user is playing against the computer.
In easy mode, the computer places random valid moves on the board. In hard mode, the computer generates all possible moves and tries to make the most advantageous move for it, by using the Minimax algorithm. 
## User Interface
The **Text Based Interface** of the application can be used to play the game by using the keyboard. The user inputs the row and column where he wants to place the symbol, while the computer makes it's move automatically after the user. The board is updated after each move and displayed using Texttable.\
The **GUI** was made using the pygame library and the user can play the game with his mouse by clicking on the board. The first window allows the user to choose the desired board size and difficulty, while the second window displays the board and allows the user to play the game and finally, the last window shows who is the winner of the game (user or computer).
## Minimax AI algorithm
