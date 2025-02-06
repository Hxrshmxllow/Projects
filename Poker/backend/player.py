class Player:
    def __init__(self, name, blind):
        self.name = name
        self.hand = []
        self.money = 1000.00
        self.blind = blind
        self.points = 0
        self.move = ""
        
    def subtract_blind(self):
        if self.blind == "Big":
            self.money -= 20
        else:
            self.money -= 10
    
    def get_blind(self):
        return self.blind
    
    def set_blind(self, blind):
        self.blind = blind
        if blind == "Small":
            self.money -= 10.00
        else:
            self.money -= 20.00
    
    def add_card(self, card):
        self.hand.append(card)
    
    def get_hand(self):
        return self.hand
    
    def callAmount(self, amount):
        self.money -= amount
    
    def raiseAmount(self, amount):
        self.money -= amount

    def reset_hand(self):
        self.hand = []