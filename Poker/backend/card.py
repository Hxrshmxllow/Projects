class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.img = rank + "_of_" + suit + ".png"
    
    def get_img(self):
        return self.img