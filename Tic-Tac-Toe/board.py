class Board():
    markers = {
        -1: ' O ',
        0: '   ',
        1: ' X '
    }

    def __init__(self):
        # -1 represents X, 0 represents empty square, 1 represents O
        self.board = [[0 for row in range(3)] for column in range(3)] #initializes a 3 x 3 board
    
    def display(self):
        for row in range(3):
            parsedRow = [board.markers[x] for x in self.board[row]]
            print('|'.join(parsedRow))
            if row < 2:
                print("---|---|---")
    
    def placeMarker(self, row, column, marker):
        for key in self.markers:
            if self.markers[key] == marker:
                marker = key
        self.board[row][column] = marker
        
    def checkSpotIsEmpty(self, row, column, marker):
        for key in self.markers:
            if self.markers[key] == marker:
                marker = key
        if self.board[row][column] == 0:
            return True
        else:
            return False

    def checkWin(self):
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != 0: #checks all the rows
                print('Row')
                return True
        for column in range(3):
            col = [self.board[0][column], self.board[1][column], self.board[2][column]]
            if col.count(col[0]) == 3 and col[0] != 0: #checks all columns
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0: #checks right-left diagonal
            return True
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0: #checks left-right diagonal
            return True
        return False
    
    def reset(self):
        self.board = [[0 for row in range(3)] for column in range(3)]

board = Board()
board.placeMarker(0, 0, ' X ')
board.placeMarker(1, 1, ' X ')
board.placeMarker(2, 2, ' X ')
board.display()
print(board.checkWin())