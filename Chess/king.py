from piece import Piece
from queen import Queen
from rook import Rook
from knight import Knight
from bishop import Bishop
from pawn import Pawn

class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color)
        if self.color == "Black":
            self.image = "pieces/black-king.png"
        else:
            self.image = "pieces/white-king.png"
        self.row = row
        self.col = col
        self.underAttack = False
        
    
    def valid_moves(self, board, player):
        moves = [
            [-1, -1],
            [-1, 0],
            [-1, 1],
            [0, -1],
            [0, 1],
            [1, -1],
            [1, 0],
            [1, 1]
        ]
        for move in moves:
            row = self.row + move[0]
            col = self.col + move[1]
            if 0 <= row < 8 and 0 <= col < 8 and (board[row][col].piece is None or board[row][col].piece.color != player.color):
                player.add_possible_move(row, col)

    def check_if_under_attack(self, game, board, player):
        moves = [
            [-1, -1, 1],
            [-1, 0, 0],
            [-1, 1, 1],
            [0, -1, 0],
            [0, 1, 0],
            [1, -1, 1],
            [1, 0, 0],
            [1, 1, 1],
            [-1, -2, 2],
            [-1, 2, 2],
            [-2, -1, 2],
            [-2, 1, 2],
            [2, -1, 2],
            [2, 1, 2],
            [1, -2, 2],
            [1, 2, 2]
        ]
        for move in moves:
            row = self.row + move[0]
            col = self.col + move[1]
            path_type = move[2] #0 if straight and 1 if diagonal and 2 if checking knight
            if 0 <= row < 8 and 0 <= col < 8:
                if path_type == 2:
                    if board[row][col].piece is not None and isinstance(board[row][col].piece, Knight) and board[row][col].piece.color != player.color:
                        self.underAttack = True
                        board[row][col].piece.isAttacking = True
                        game.add_piece_in_action(self.row, self.col)
                        game.add_piece_in_action(row, col)
                else:
                    if board[row][col].piece is None: #search if threat in direction
                        row += move[0]
                        col += move[1]
                        while 0 <= row < 8 and 0 <= col < 8: 
                            if board[row][col].piece is not None: #if any piece is found
                                if board[row][col].piece.color != player.color: #if opponent piece found
                                    if (path_type == 0 and isinstance(board[row][col].piece, (Queen, Rook))) or (path_type == 1 and isinstance(board[row][col].piece, (Queen, Bishop))):
                                        self.underAttack = True
                                        board[row][col].piece.isAttacking = True
                                        game.add_piece_in_action(self.row, self.col)
                                        game.add_piece_in_action(row, col)
                                break
                            else:
                                row += move[0]
                                col += move[1]
                    elif board[row][col].piece.color != player.color: #check is threat if in proximity (1 block)
                        if (path_type == 0 and isinstance(board[row][col].piece, (King, Queen, Rook))) or (path_type == 1 and isinstance(board[row][col].piece, (King, Queen, Bishop, Pawn))):
                            self.underAttack = True
                            board[row][col].piece.isAttacking = True
                            game.add_piece_in_action(self.row, self.col)
                            game.add_piece_in_action(row, col)

                
