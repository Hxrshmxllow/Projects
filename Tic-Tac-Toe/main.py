from player import Player
from board import Board

def main():
    board = Board()
    humanName = input("What is your name: ")
    humanMarker = input('What marker would you like to be (X or O): ')
    if 'X' in humanMarker:
        human = Player(humanName, -1)
        AI = Player('AI', 1)
    else:
        human = Player(humanName, 1)
        AI = Player('AI', -1)
        

    
