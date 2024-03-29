# minesweeperAI
An AI that can beat Minesweeper using a knowledge base.

With each turn, the AI will build upon a knowledge base of 'sentences'. Each sentence has information on a space's count of surrounding mines, making it possible for the AI to make inferences on which spaces are mines and which are safe, given enough knowledge. 


## How to run the program
`python3`

`exec(open("runner.py).read())`


## How does the program work?

### In minesweeper.py ...

... there are 3 main classes:
1. **Minesweeper** - handles the game mechanics such as the numbers, adding mines on the board, checking when game is won. (not implemented by me)
2. **Sentence** - creates a 'sentence' to then be stored in the knowledge base. (known_mines, known_safes, mark_mine, mark_safe implemented by me)
3. **MinesweeperAI** - this is the AI which makes moves by itself and finds out safe spaces for the next turn and mines to avoid/flag. (mark_mine, mark_safe, add_knowledge, make_safe_move, make_random_move implemented by me)

### Knowledge is represented like so:

![middle_safe](https://user-images.githubusercontent.com/65613196/141170685-3115890c-5e66-44bd-aee8-724bce546884.png)

{A, B, C, D, E, F, G, H} = 1

This sentence tells us that out of all of these cells, one of them is a mine.

## How the AI works

Safe cells can be easily deduced when the count of a revealed cell is 0. When this happens, all the surrounding cells are added to a set of 'safes'.

Safe cells can also be deduced if the number of available spaces matches the count (e.g. if the count is 2 and no mines have been found in the surrounding cells and there are 2 black spaces remaining, we can assume they are both mines). 

Lastly, safe cells can be deduced when multiple counts overlap eachother using a more **advanced inference**. Here we can see that {A, B, C} = 1 and {A, B, C, D, E} = 2

![subset_inference](https://user-images.githubusercontent.com/65613196/141172452-040a2060-2605-4e26-97a4-b14ed17bd3ed.png)

These sentences can be combined to infer a new sentence: {D, E} = 1 which makes it easier down the line. If, for instance, we find out later that E is a safe, we then know D is a mine whereas if the sentence was left as {A, B, C, D, E} = 2 we would not have been able to infer that. 

Using the knowledge base of many different sentences like the ones above, the AI makes deductions using the behaviours mentioned above until all possible inferences are made. If all possible inferences have been made and there are no known safe spaces to make, the AI will make a random move on the board. 


Visit http://tomchoi.co.uk/minesweeper-ai/ to see a video of it in action.


### runner.py ...

... is how the game runs on Pygame. Here you will find how the screen is drawn out, how the buttons work and how it integrates with mineswepper.py to call on its functions. This was not implemented by me. Only lines 166 and 167 were added by me so that flags are shown when the AI finds mines. 


