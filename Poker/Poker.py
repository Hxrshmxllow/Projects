import random
from collections import Counter

class Poker():
    suits = ["Spade", "Heart", "Club", "Diamond"]
    ranks = [i for i in range(2,11)] + ["J", "Q", "K", "A"]

    def __init__(self):
        self.players = []
        self.communityCards = []
        self.pot = 0.00
        self.deck = []
        self.round = "Pre-Flop"
        self.potRaised = True
        self.raiseAmount = 10.00

    def resetDeck(self):
        self.communityCards = []
        for player in self.players:
            player.hand = []
        self.deck = [Card(suit, rank, Poker.ranks.index(rank) + 1) for suit in Poker.suits for rank in Poker.ranks]
    
    def blind(self):
        self.players.reverse()
        blind = 10.00
        self.potRaised = True
        self.raiseAmount = 10.00
        for player in self.players:
            player.money -= blind
            blind += 10.00

    def printGame(self):
        print("-------------------")
        for player in self.players:
            print(f"{player.name} Money: ${player.money}")
            print(f"{player.name} Cards:")
            for card in player.hand:
                print(f"{card.suit} {card.rank}")
            print()
        print("Community Cards: ")
        if self.round != "Pre-Flop":
            for card in self.communityCards:
                print(f"{card.suit} {card.rank}")
        else:
            print("None")
        print("-------------------")

    def raisePot(self, player, amount):
        player.money -= amount
        self.pot += amount
        if self.potRaised:
            player.money -= self.raiseAmount
            self.pot += self.raiseAmount
        self.potRaised = True
        self.raiseAmount = amount

    def call(self, player):
        print("player called")
        player.money -= self.raiseAmount
        self.pot += self.raiseAmount
        self.potRaised = False
        self.raiseAmount = 0.00

    def fold(self, player):
        for winner in self.players:
            if winner != player:
                winner.money += self.pot
                break
        self.pot = 0.00 

    def bet(self, recalled, playerRaised):
        if recalled:
            for player in self.players:
                if player != playerRaised:
                    options = {1: "Raise", 2: f"Call ${self.raiseAmount}", 3: "Fold"}
                    for option in options:
                        print(f"{option}. {options[option]}")
                    choice = int(input(f"What would {player.name} like to do? "))
                    if options[choice] == "Raise":
                        amount = float(input("How much would you like to raise: $"))
                        self.raisePot(player, amount)
                        self.bet(True, player)
                    elif options[option] == f"Call ${self.raiseAmount}":
                        self.call(player)
                    elif options[option] == "Fold":
                        self.fold(player)
                        return True
                    return False
        else:
            for player in self.players:
                options = {1: "Raise", 2: "Check", 3: "Fold"}
                if self.potRaised:
                    options[2] = f"Call ${self.raiseAmount}"
                for option in options:
                    print(f"{option}. {options[option]}")
                choice = int(input(f"What would {player.name} like to do? "))
                if options[choice] == "Raise":
                    amount = float(input("How much would you like to raise: $"))
                    self.raisePot(player, amount)
                elif options[choice] == "Check":
                    continue
                elif options[choice] == "Fold":
                    self.fold(player)
                    return True
                elif options[choice] == f"Call ${self.raiseAmount}":
                    self.call(player)
                if player == self.players[1] and self.potRaised:
                    return self.bet(True, player)
            return False
    
    def preFlop(self):
        self.round = "Pre-Flop"
        self.pot = 0.00
        self.resetDeck()
        self.blind()
        for i in range(2): 
            for player in self.players:
                player.highCard = False
                player.points = 0
                card = random.choice(self.deck)
                player.hand.append(card)
                self.deck.remove(card)
        self.printGame()
        return self.bet(False, None)
    
    def flop(self):
        self.round = "Flop"
        for i in range(3):
            card = random.choice(self.deck)
            self.communityCards.append(card)
            self.deck.remove(card)
        self.printGame()
        return self.bet(False, None)
    
    def turn(self):
        self.round = "Turn"
        card = random.choice(self.deck)
        self.communityCards.append(card)
        self.deck.remove(card)
        self.printGame()
        return self.bet(False, None)

    def river(self):
        self.round = "River"
        card = random.choice(self.deck)
        self.communityCards.append(card)
        self.deck.remove(card)
        self.printGame()
        if self.bet(False, None):
            return
        else:
            self.checkWin()
            return 
    
    def checkWin(self):
        for player in self.players:
            if player.name == "AI":
                ai = player
            else:
                human = player
        humanHighCard = max([card.value for card in human.hand])
        aiHighCard = max([card.value for card in ai.hand])
        #check pairs (one pair, two pair, three of kind, four of kind, full house)
        counter = Counter(communityCards)
        most_common_count = counter.most_common(1)[0][1] #checks pairs in community cards
        for player in self.players:
            cards = [card.rank for card in player.hand]
            communityCards = [card.rank for card in self.communityCards]
            if cards[0] == cards[1]:
                player.points = 1 #1 pair
                if communityCards.count(cards[0]) == 2: #four of kind
                    player.points = 7
                elif most_common_count == 3: #full house
                    player.points = 6
                elif communityCards.count(cards[0]) == 1: #three of kind
                    player.points = 3
                elif most_common_count == 2: #two pair
                    player.points = 2
            else:
                for card in cards:
                    if player.points + self.communityCards.count(card) == 3: #full house
                        player.points = 6
                    elif communityCards.count(card) == 2: #three of kind
                        player.points = 3
                    elif player.points + communityCards.count(card) == 2: #two pair
                        player.points = 2
                    else:
                        player.points += communityCards.count(card)
        for player in self.players:
            cards = [card.suit for card in player.hand] + [card.suit for card in self.communityCards]
            counter = Counter(communityCards)
            most_common_count = counter.most_common(1)[0][1]
            if most_common_count >= 5 and player.points < 5:
                player.points = 5

        


class Card():
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

class Player():
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hand = []
        self.points = 0
        self.highCard = False

def main():
    game = Poker()
    print("Welcome to Poker! Each player starts off with $1000.00.")
    human = Player(input("Enter your name: "), 1000.00)
    print("You are small blind.")
    ai = Player("AI", 1000.00)
    game.players = [ai, human]
    run = True
    while run and 0 not in [player.money for player in game.players]:
        if game.preFlop() is False:
            if game.flop() is False:
                if game.turn() is False:
                    game.river()

if __name__ == "__main__":
    main()