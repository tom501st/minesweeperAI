# minesweeperAI
An AI that can beat Minesweeper using a knowledge base.

With each turn, the AI will build upon a knowledge base of 'sentences'. Each sentence has information on a space's count of surrounding mines, making it possible for the AI to make inferences on which spaces are mines and which are safe, given enough knowledge. 


## How to run the program
`python3`

`exec(open("runner.py).read())`


## How does the program work?

### In minesweeper.py ...

... there are 3 main classes;
1. Minesweeper - handles the game mechanics such as the numbers, adding mines on the board, checking when game is won. (not implemented by me)
2. Sentence - creates a 'sentence' to then be stored in the knowledge base. (known_mines, known_safes, mark_mine, mark_safe implemented by me)
3. MinesweeperAI - this is the AI which makes moves by itself and finds out safe spaces for the next turn and mines to avoid/flag. (mark_mine, mark_safe, add_knowledge, make_safe_move, make_random_move implemented by me)

### In runner.py ...

... there are 


