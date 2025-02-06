class Game():
    def __init__(self, x, o):
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.x = x
        self.o = o
        self.curr_player = x
        self.win = None
    
    def switch_curr_player(self):
        if self.curr_player == self.x:
            self.curr_player = self.o
        else:
            self.curr_player = self.x
    
    def get_sqaure_img(self, row, col):
        if self.board[row][col] == 1:
            return self.x.img
        elif self.board[row][col] == -1:
            return self.o.img
        else:
            return None
        
    def change_square(self, row, col):
        self.board[row][col] = self.curr_player.num

    def check_for_win(self):
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != 0: #checks all the rows
                self.win = ['row', row]
                return True
        for column in range(3):
            col = [self.board[0][column], self.board[1][column], self.board[2][column]]
            if col.count(col[0]) == 3 and col[0] != 0: #checks all columns
                self.win = ['col', col]
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0: #checks right-left diagonal
            self.win = ['diagonal', 0]
            return True
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0: #checks left-right diagonal
            self.win = ['diagonal', 1]
            return True
        return False

class Player():
    def __init__(self, type):
        if type == -1:
            self.img = 'pieces/o.png'
            self.num = -1
        else:
            self.img = 'pieces/x.png'
            self.num = 1


