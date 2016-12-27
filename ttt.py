from itertools import cycle
import argparse

class Board(object):
    def __init__(self, size):
        self.size = size
        self.board = [size * [None] for x in range(size)] 
    
    def __getitem__(self, coords):
        '''
        Returns what's in the requested position
        '''
        x, y = coords
        return self.board[x][y]
    
    def __setitem__(self, coords, player):
        '''
        Sets a position to a player's marker
        '''
        x, y = coords
        self.board[x][y] = player
    
    def __repr__(self):
        '''
        Print a representation of the board
        '''
        def row_string(row):
            values = [self[x, row] for x in range(self.size)]
            return " | ".join(" " if x is None else str(x) for x in values)
            
        rows = [row_string(row) for row in range(self.size)]
        
        lines = "\n" + "-" * len(rows[0]) + "\n"
                
        return lines.join(rows)

    def winner_for_coords(self, coords):
        '''
        Check if there's a winner given a list of coordinates
        '''
        values = [self[coord] for coord in coords]
        if len(set(values)) == 1 and None not in values:
            return values[0]
        else:
            return None        
                
    def winning_combinations(self):
        '''
        Generate list of lists, each of which is a winning condition 
        '''
        nums = range(self.size) # can use for both rows and columns
        
        winning_combinations = []
        
        # add the diagonals
        winning_combinations.append(list(zip(nums, nums)))
        winning_combinations.append(list(zip(nums, reversed(nums))))
        
        # add the winning rows and columns
        for row in nums:
            rows = [row] * self.size
            winning_combinations.append(list(zip(rows, nums)))
            winning_combinations.append(list(zip(nums, rows)))    
        
        return winning_combinations

    def winner(self, player):
        '''
        Check if any of the win conditions have been satisfied
        '''
        return any(player == self.winner_for_coords(combo) for combo in self.winning_combinations())

class Player(object):
    def __init__(self, num, marker):
        self.num = num
        self.marker = marker
    
    def __str__(self):
        '''
        Representation of the player for printing on the board
        '''
        return self.marker

    def turn(self, board):
        '''
        Does the player's turn. Prompts again if invalid input is entered.
        '''
        while True:
            player_input = input("Player {}: Enter some coordinates. ".format(self.num))
        
            try:
                x, y = [int(num) for num in player_input.split(",")]
            
                if board[x, y] is None:
                    board[x, y] = self
                    break
            
                else:
                    print("That spot's taken by Player {}.".format(board[x, y].num))
        
            except (ValueError, IndexError):
                print("“{}” is invalid.".format(player_input))

# use arg to request board dimensions
parser = argparse.ArgumentParser()
parser.add_argument("--size", default = 3, type = int, help = "Size of board")
args = parser.parse_args()

# set up the game 
player1 = Player(1, "X")
player2 = Player(2, "O")
board = Board(args.size)

print("Player 1 is X and Player 2 is O. Player 1 goes first.")

for player in cycle([player1, player2]):
    player.turn(board)
    
    print(board)
    if board.winner(player):
        print("Player {} wins!".format(player.num))
        break
