import os
import sys
import random


def split_board(board):
    """ split board for possible winning combinations """
    row1 = board[0]
    row2 = board[1]
    row3 = board[2]
    diag1 = [row1[0], row2[1], row3[2]]
    diag2 = [row1[2], row2[1], row3[0]]
    col1 = [row1[0], row2[0], row3[0]]
    col2 = [row1[1], row2[1], row3[1]]
    col3 = [row1[2], row2[2], row3[2]]
    return [row1, row2, row3, diag1, diag2, col1, col2, col3]   


class Player:
    id = 0
    def __init__(self, token, AI=None):
        Player.id += 1
        self.p_id = Player.id
        self.token = token
        if AI is None:
            self.AI = False
        else:
            self.AI = True  

    def could_win(self, three):
        could_win = False
        token_count = 0
        for elem in three:
            if elem == self.token:
                token_count += 1
        if token_count == 2:
            could_win = True
        return could_win

    def should_block(self, three):
        should_block = False
        token_count = 0
        for elem in three:
            if not isinstance(elem, int) and elem != self.token:
                token_count += 1
        if token_count == 2:
            should_block = True
        return should_block        

    def look_for_2of3(self, board):
        """ look for 2 of 3"""
        threes = split_board(board)
        best_move_is_in = -1
        best_move = -1
        winning_move = -1
        for elem in threes:
            if self.could_win(elem):
                best_move_is_in = elem
                for i in elem:
                    if isinstance(i, int):
                        winning_move = i
                        best_move = winning_move
        if winning_move == -1:
            for elem in threes:
                if self.should_block(elem):
                    best_move_is_in = elem
                    for i in elem:
                        if isinstance(i, int):
                            best_move = i
        return best_move      
                            
    def has_diag_win(self, board):
        has_win = False
        row1 = board[0]
        row2 = board[1]
        row3 = board[2]
        if row1[0] == row2[1] and row2[1] == row3[2]:
            has_win = True
        if row1[2] == row2[1] and row2[1] == row3[0]:
            has_win = True
        return has_win

    def has_vert_win(self, board):
        has_win = False
        row1 = board[0]
        row2 = board[1]
        row3 = board[2]
        if row1[0] == row2[0] and row2[0] == row3[0] and row1[0] == self.token:
            has_win = True
        if row1[1] == row2[1] and row2[1] == row3[1] and row1[1] == self.token:
            has_win = True
        if row1[2] == row2[2] and row2[2] == row3[2] and row1[2] == self.token:
            has_win = True
        return has_win

    def has_horiz_win(self, board):
        has_win = False
        for r in board:
            if r[1:] == r[:-1] and r[1] == self.token:
                print("Horizontal win found.")
                has_win = True
        return has_win

    def has_won(self, board):
        if self.has_diag_win(board) or self.has_vert_win(board) \
                or self.has_horiz_win(board):
            return True  

    def make_move(self, board):
        valid_move = False
        move = input("\nPlayer " + str(self.p_id) 
            + ", please enter the number of the space where you would like to move: ")
        for r in board:
            if move in r:
                loc = r.index(move)
                r[loc] = self.token
                valid_move = True
        if not valid_move:
            print("That was not a valid move -- please try again.")
            self.make_move(board)
        return move

    def make_AI_move(self, board, available_spots):
        print("\nAI opponent's move:")
        best_move = self.look_for_2of3(board)
        if best_move == -1:
            if 1 in available_spots:
                best_move = 1
            elif 5 in available_spots:
                best_move = 5
            else:
                best_move = random.choice(available_spots)
        for r in board:
            if best_move in r:
                loc = r.index(best_move)
                r[loc] = self.token    
        return best_move

    def move(self, board, avail_spots):
        if self.AI:
            best_move = self.make_AI_move(board, avail_spots)
        if not self.AI:
            best_move = self.make_move(board)
        return best_move            
    
 
class TicTacToe:
    """ 
    Game states:
    0 - Game has not started
    1 - Game is active (no player has won)
    2 - Game is over with no win
    """   
    def __init__(self, AI):
        self.board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        if not AI:
            self.p1 = Player('X')
            self.p2 = Player('O')
        if AI:
            AI_player = random.choice([1,2])
            if AI_player == 1:
                self.p1 = Player('X', True)
                self.p2 = Player('O')
            else:
                self.p1 = Player('X')
                self.p2 = Player('O', True) 
        self.game_over = False
        self.game_state = 0
        self.whose_turn = 1
        self.turn_counter = 0
        self.available_spots = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def print_board(self):
        print(" --- --- --- ")
        for e in self.board:
            print("|"),
            print(" | ".join(str(item) for item in e)),
            print("|")
            print(" --- --- --- ")

    def exit_game(self):
        print("The game is over! Thanks for playing.")
        self.print_board()
        quit()     
                
    def play(self):
        if self.p1.AI or self.p2.AI:
            if self.p1.AI:
                print("Playing with an AI opponent -- AI opponent has first move.")
            else:
                print("Playing with an AI oppenent -- you have first move.")
        else:
            print("Playing with two human players.")    
        while self.game_state == 1:
            if self.whose_turn == 1:
                self.whose_turn = 2
                self.print_board()
                move = self.p1.move(self.board, self.available_spots)
                self.available_spots.remove(move)
                self.turn_counter += 1
                if self.p1.has_won(self.board):
                    print("WINNER IS PLAYER 1")
                    self.exit_game()
            if self.turn_counter > 8:
                print("We have a scratch -- no winner.")
                self.exit_game()    
            if self.whose_turn == 2:
                self.whose_turn = 1
                self.print_board()
                move = self.p2.move(self.board, self.available_spots)
                self.available_spots.remove(move)
                self.turn_counter += 1
                if self.p2.has_won(self.board):
                    print("WINNER IS PLAYER 2")
                    self.exit_game()


def start():
    print(
        """\n=========================\n= Welcome to TicTacToe! =\
        \n=========================\n""")
    game_type = input(
        '\nPlease enter 0 to play with another human or 1 to play with AI: ')
    if game_type == 0:
        game = TicTacToe(False)
    elif game_type == 1:
        game = TicTacToe(True)  
    game.game_state += 1
    print(
        """\nThe numbers printed below represent the board spaces.\
        \nTo move, each player will enter the number of the space \
        \nwhere you would like to place your X or O.\n""")   
    game.play()
        

if __name__ == "__main__":
    start()
