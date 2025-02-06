from piece import Piece

class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color)
        if self.color == "Black":
            self.image = "pieces/black-pawn.png"
        else:
            self.image = "pieces/white-pawn.png"
        self.row = row
        self.col = col
    
    def valid_moves(self, board, player):
        if self.color == "White":
            if self.row == 6 and board[4][self.col].piece is None:
                player.add_possible_move(4, self.col)
            if self.row - 1 > -1 and board[self.row - 1][self.col].piece is None:
                player.add_possible_move(self.row - 1, self.col)
            if self.row - 1 > -1 and self.col - 1 > -1 and board[self.row - 1][self.col - 1].piece is not None and board[self.row - 1][self.col - 1].piece.color != player.color:
                player.add_possible_move(self.row - 1, self.col - 1)
            if self.row - 1 > -1 and self.col + 1 < 8 and board[self.row - 1][self.col + 1].piece is not None and board[self.row - 1][self.col + 1].piece.color != player.color:
                player.add_possible_move(self.row - 1, self.col + 1)
        else:
            if self.row == 1 and board[3][self.col].piece is None:
                player.add_possible_move(3, self.col)
            if self.row + 1 < 8 and board[self.row + 1][self.col].piece is None:
                player.add_possible_move(self.row + 1, self.col)
            if self.row + 1 < 8 and self.col - 1 > -1 and board[self.row + 1][self.col - 1].piece is not None and board[self.row + 1][self.col - 1].piece.color != player.color:
                player.add_possible_move(self.row + 1, self.col - 1)
            if self.row + 1 < 8 and self.col + 1 < 8 and board[self.row + 1][self.col + 1].piece is not None and board[self.row + 1][self.col + 1].piece.color != player.color:
                player.add_possible_move(self.row + 1, self.col + 1)
            
