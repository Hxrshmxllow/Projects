class Player:
    def __init__(self, color):
        self.color = color
        self.pawn1 = None
        self.pawn2 = None
        self.pawn3 = None
        self.pawn4 = None
        self.pawn5 = None
        self.pawn6 = None
        self.pawn7 = None
        self.pawn8 = None
        self.rook1 = None
        self.knight1 = None
        self.bishop1 = None
        self.queen = None
        self.king = None
        self.rook2 = None
        self.knight2 = None
        self.bishop2 = None
        self.possible_moves = []
        self.selected_piece = []
    
    def reset_selected_piece(self):
        self.selected_piece = []

    def select_piece(self, row, col):
        self.selected_piece = [row, col]    

    def add_possible_move(self, row, col):
        self.possible_moves.append([row, col])
    
    def reset_possible_moves(self, board):
        if len(self.possible_moves) > 0:
            for move in self.possible_moves:
                row = move[0]
                col = move[1]
                board[row][col].highlighted = False
        self.possible_moves = []