# Obstruction
## Game overview
The game "Obstruction" looks similar to tic-tac-toe, but it's main point is to cover the whole board in 'X', '0' and obstructed squares '/'. The winner is the last player who puts a symbol on the board.
The game can be played using the text-based interface, or the GUI. It has 5 different board sizes available and 2 difficulties: easy and hard, where the user is playing against the computer.
In easy mode, the computer places random valid moves on the board. In hard mode, the computer generates all possible moves and tries to make the most advantageous move for it, by using the Minimax algorithm. 
## User Interface
The **Text Based Interface** of the application can be used to play the game by using the keyboard. The user inputs the row and column where he wants to place the symbol, while the computer makes it's move automatically after the user. The board is updated after each move and displayed using Texttable.\
The **GUI** was made using the pygame library and the user can play the game with his mouse by clicking on the board. The first window allows the user to choose the desired board size and difficulty, while the second window displays the board and allows the user to play the game and finally, the last window shows who is the winner of the game (user or computer).
## Minimax AI algorithm
The minimax algorithm is a decision making algorithm, which computes all the possible moves with the computer being the maximizer and the user being the minimizer. The computer updates the board by assuming that the user plays as good as he can and gets all possible outcomes, from which he chooses the one with the best outcome for the maximizer.\ 
For my algorithm I used:
- _depth factor_ - Limits how many moves ahead the AI looks by rewarding faster wins and penalazing slower losses. Lower depth = faster but less strategic. Higher depth = more strategic but slower.\
- _alpha-beta pruning_ - Prunes the remaining branches when beta <= alpha, meaning that we don't need to check them anymore. Alpha: The best score that the maximizer (computer) is guaranteed so far. Beta: The best score that the minimizer (user) is guaranteed so far.\
- _heuristic evaluation_ - Prioritizes the center and blocks human's potential moves.
