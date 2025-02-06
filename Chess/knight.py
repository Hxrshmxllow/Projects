from piece import Piece

class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color)
        if self.color == "Black":
            self.image = "pieces/black-knight.png"
        else:
            self.image = "pieces/white-knight.png"
        self.row = row
        self.col = col

    def valid_moves(self, board, player):
        moves = [
            [-1, -2],
            [-1, 2],
            [-2, -1],
            [-2, 1],
            [2, -1],
            [2, 1],
            [1, -2],
            [1, 2]
        ]
        for move in moves:
            row = self.row + move[0]
            col = self.col + move[1]
            if (0 <= row < 8 and 0 <= col < 8) and (board[row][col].piece is None or board[row][col].piece.color != player.color):
                player.add_possible_move(row, col)