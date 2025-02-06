class Sqaure:
    def __init__(self, row, col, piece, color):
        self.row = row
        self.col = col
        self.piece = piece
        self.color = color
        self.highlighted = False
    
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.piece = None
        self.color = color
        self.highlighted = False