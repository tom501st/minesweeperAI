import itertools
import random
import time


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells) and self.count != 0:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            if cell in sentence.cells:
                sentence.remove(cell) 

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            if cell in sentence.cells:
                sentence.remove(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1) mark the cell as a move that has been made
        # 2) mark the cell as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        #    based on the value of `cell` and `count`

        # create a set of the move's surrounding cells
        surrounding_cells = set()
        for i in range(-1, 2):
            new_i = cell[0]
            new_i += i
            for j in range(-1, 2):
                new_j = cell[1]
                new_j += j
                # Ignore surrounding cell if it's out of bounds and also, exclude the move (i.e cell)
                if new_i < 0 or new_j < 0 or (new_i, new_j) == cell or new_i > (self.height -1) or new_j > (self.width -1):
                    continue
                # avoid adding any known mines in set. Decrement count if a mine is present so that the sentence is correct. 
                if (new_i, new_j) in self.mines:
                    count -= 1
                    continue
                # avoid adding any known safes in set.
                if (new_i, new_j) in self.safes:
                    continue
                else:
                    surrounding_cells.add((new_i, new_j))
        
        # add the sentence to the knowledge base (e.g. "{(5, 0), (3, 1), (4, 1), (5, 1), (3, 0)} = 0)" )
        self.knowledge.append(Sentence(surrounding_cells, count))

        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base

        # mark any safes or mines we can deduce using the known_safes and known_mines functions
        safes = set()
        mines = set()
        for sentence in self.knowledge:   
            # if known_safes is not empty, add the safes to the 'safes' set using the mark_safe function. Do the same for the mines.
            if sentence.known_mines():
                mines = self.mines.union(sentence.known_mines())
                for mine in mines:
                    self.mark_mine(mine)
            if sentence.known_safes():
                # create separate/duplicate set for safes and mines to stop 'Set changed size during iteration' error
                safes = self.safes.union(sentence.known_safes())
                for safe in safes:
                    self.mark_safe(safe)
        # now all obvious mines and safes are marked in the KB


        # 5) add any new sentences to the AI's knowledge base
        #    if they can be inferred from existing knowledge

        # make advanced inferences by checking if any sentences are 
        # subsets of other sentences, then subtracting the difference
        # e.g. if we have {A, B, C, D} = 2 and {C, D} = 1
        # we can infer that {A, B} = 1
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence2 != sentence1:
                    cells1 = sentence1.cells
                    cells2 = sentence2.cells
                    if cells1.issubset(cells2):
                        cells2 -= cells1
                        sentence2.count -= sentence1.count


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                self.moves_made.add(safe)
                return safe
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        takenSpaces = self.moves_made.union(self.mines)
        availableSpaces = []

        # make a list of all available spaces and choose one randomly
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in takenSpaces:
                    availableSpaces.append((i, j))
        if len(availableSpaces) == 0:
            print('GAME WON, AVAILABLE SPACES EXHAUSTED. RESET GAME TO PLAY AGAIN.')
            return None
        print('MAKING RANDOM MOVE')
        return random.choice(availableSpaces)