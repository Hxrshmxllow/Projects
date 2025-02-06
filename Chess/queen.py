from piece import Piece

class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color)
        if self.color == "Black":
            self.image = "pieces/black-queen.png"
        else:
            self.image = "pieces/white-queen.png"
        self.row = row
        self.col = col

    def valid_moves(self, board, player):
        #diagonals
        moves = [
            [1, 1],
            [1, -1],
            [-1, 1],
            [-1, -1]
        ]
        for move in moves:
            row = self.row + move[0]
            col = self.col + move[1]
            while 0 <= row < 8 and 0 <= col < 8:
                if board[row][col].piece is not None:
                    if board[row][col].piece.color != player.color:
                        player.add_possible_move(row, col)
                    break
                player.add_possible_move(row, col)
                row += move[0]
                col += move[1]
        #straights
        moves = [
            [1, 0],
            [-1, 0],
            [0, 1],
            [0, -1]
        ]
        for move in moves:
            row = self.row + move[0]
            col = self.col + move[1]
            while 0 <= row < 8 and 0 <= col < 8:
                if board[row][col].piece is not None:
                    if board[row][col].piece.color != player.color:
                        player.add_possible_move(row, col)
                    break
                player.add_possible_move(row, col)
                row += move[0]
                col += move[1]