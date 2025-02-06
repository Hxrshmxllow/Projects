from sqaure import Sqaure
from player import Player
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King
from pawn import Pawn

class Game:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            if row % 2 == 0: #IF ROW IS EVEN, START OFF WITH WHITE SQUARE
                color = "White"
            else:
                color = "Black"
            for col in range(8):
                self.board[row][col] = Sqaure(row, col, color)
                if color == "Black":
                    color = "White"
                else:
                    color = "Black"
        self.black = Player('Black')
        self.white = Player('White')
        self.curr_player = self.white
        self.pieces_in_action = []
        self.__initBlack__()
        self.__initWhite__()
    
    def __initBlack__(self):
        #initialzing rooks
        self.black.rook1 = Rook("Black", 0, 0)
        self.black.rook2 = Rook("Black", 0, 7)
        self.board[0][0].piece = self.black.rook1
        self.board[0][7].piece = self.black.rook2

        #initializing knights
        self.black.knight1 = Knight("Black", 0, 1)
        self.black.knight2 = Knight("Black", 0, 6)
        self.board[0][1].piece = self.black.knight1
        self.board[0][6].piece = self.black.knight2

        #initializing bishops
        self.black.bishop1 = Bishop("Black", 0, 2)
        self.black.bishop2 = Bishop("Black", 0, 5)
        self.board[0][2].piece = self.black.bishop1
        self.board[0][5].piece = self.black.bishop2

        #initializing queen
        self.black.queen = Queen("Black", 0, 3)
        self.board[0][3].piece = self.black.queen

        #initializing king
        self.black.king = King("Black", 0, 4)
        self.board[0][4].piece = self.black.king

        #initializing pawns
        for col in range(8):
            pawn = Pawn("Black", 1, col) 
            self.board[1][col].piece = pawn 
            setattr(self.black, f"pawn{col + 1}", pawn)

    def __initWhite__(self):
        #initialzing rooks
        self.white.rook1 = Rook("White", 7, 0)
        self.white.rook2 = Rook("White", 7, 7)
        self.board[7][0].piece = self.white.rook1
        self.board[7][7].piece = self.white.rook2

        #initializing knights
        self.white.knight1 = Knight("White", 7, 1)
        self.white.knight2 = Knight("White", 7, 6)
        self.board[7][1].piece = self.white.knight1
        self.board[7][6].piece = self.white.knight2

        #initializing bishops
        self.white.bishop1 = Bishop("White", 7, 2)
        self.white.bishop2 = Bishop("White", 7, 5)
        self.board[7][2].piece = self.white.bishop1
        self.board[7][5].piece = self.white.bishop2

        #initializing queen
        self.white.queen = Queen("White", 7, 4)
        self.board[7][4].piece = self.white.queen

        #initializing king
        self.white.king = King("White", 7, 3)
        self.board[7][3].piece = self.white.king

        #initializing pawns
        for col in range(8):
            pawn = Pawn("White", 6, col) 
            self.board[6][col].piece = pawn 
            setattr(self.white, f"pawn{col + 1}", pawn)

    def switch_player(self):
        if self.curr_player == self.black:
            self.curr_player = self.white
        else:
            self.curr_player = self.black

    def add_piece_in_action(self, row, col):
        self.pieces_in_action.append([row, col])
    
    def remove_pieces_in_action(self):
        for piece in self.pieces_in_action:
            row = piece[0]
            col = piece[1]
            if isinstance(self.board[row][col].piece, King):
                self.board[row][col].piece.underAttack = False
            elif self.board[row][col].piece is not None:
                self.board[row][col].piece.isAttacking = False