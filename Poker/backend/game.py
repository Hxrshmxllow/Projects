from card import Card
from player import Player
import random
from bot import *
import re
from collections import Counter

class Game:
    suits = ["spades", "diamonds", "clubs", "hearts"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]

    def __init__(self):
        self.deck = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        self.player = Player("Harshit", "Big")
        self.ai = Player("AI", "Small")
        self.communityCards = []
        self.pot = 0.00
        self.round = "Pre-Flop"
        self.bigBlind = self.player
        self.currPlayer = self.ai
        self.raised = True
        self.amountRaised = 10.00
        self.winner = None
    
    def reset(self):
        self.deck = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        self.communityCards = []
        self.pot = 30.00
        self.round = "Pre-Flop"
        if self.player.get_blind() == "Big":
            self.player.set_blind("Small")
            self.ai.set_blind("Big")
            self.bigBlind = self.ai
            self.currPlayer = self.player
        else:
            self.ai.set_blind("Small")
            self.player.set_blind("Big")
            self.bigBlind = self.player
            self.currPlayer = self.ai
        self.player.points = 0
        self.ai.points = 0
        self.raised = True
        self.amountRaised = 10.00
        self.deal_cards()
        
    def player_fold(self, player):
        if player == self.player:
            self.ai.money += self.pot
            self.winner = "AI"
        else:
            self.player.money += self.pot
            self.winner = "Player"
        self.pot = 0.00
        self.player.reset_hand()
        self.ai.reset_hand()
        self.reset()

    def deal_cards(self):
        random.shuffle(self.deck)
        for i in range(2):
            self.player.add_card(self.deck.pop(0))
            self.ai.add_card(self.deck.pop(0))
    
    def deal_community_card(self):
        self.deck.pop(0)
        self.communityCards.append(self.deck.pop(0))

    def pre_flop(self):
        self.winner = None
        self.pot = 30.00
        self.player.subtract_blind()
        self.ai.subtract_blind()
        self.deal_cards()
        if self.currPlayer == self.ai:
            self.bot_move()
        return
    
    def flop(self):
        if self.currPlayer == self.ai:
            self.bot_move()
        return
    
    def river(self):
        if self.currPlayer == self.ai:
            self.bot_move()
        return

    def bot_move(self):
        ai_card1 = self.ai.get_hand()[0]
        ai_card2 = self.ai.get_hand()[1]
        communityCard1 = self.communityCards[0] if len(self.communityCards) > 0 else None
        communityCard2 = self.communityCards[1] if len(self.communityCards) > 1 else None
        communityCard3 = self.communityCards[2] if len(self.communityCards) > 2 else None
        communityCard1Name = communityCard1.suit + " " + communityCard1.rank if communityCard1 else None
        communityCard2Name = communityCard2.suit + " " + communityCard2.rank if communityCard2 else None
        communityCard3Name = communityCard3.suit + " " + communityCard3.rank if communityCard3 else None
        data = {
            "ai_card1": ai_card1.suit + " " + ai_card1.rank,
            "ai_card2": ai_card2.suit + " " + ai_card2.rank,
            "pot": self.pot,
            "round": self.round,
            "community_card1": communityCard1Name,
            "community_card2": communityCard2Name,
            "community_card3": communityCard3Name,
            "ai_money": self.ai.money,
            "call_amount": self.amountRaised
        }
        aiMove = get_ai_move(data)
        self.ai.move = aiMove
        if "Call" in aiMove:
            self.ai.callAmount(self.amountRaised)
            self.pot += self.amountRaised
            self.amountRaised = 0.00
            self.raised = False
            self.deal_community_card()
        elif "Check" in aiMove:
            self.amountRaised = 0.00
            self.raised = False
            if self.ai.blind == "Big":
                self.deal_community_card()
        elif "Raise" in aiMove:
            amount = int(re.findall(r'\d+', aiMove)[0])
            self.amountRaised = amount
            self.ai.raiseAmount(amount)
            self.pot += amount
            self.raised = True
        elif "Fold" in aiMove:
            self.amountRaised = 0.00
            self.raised = False
            self.player_fold(self.ai)
    
    def player_move(self, move, amount):
        if move == "check":
            self.amountRaised = 0.00
            self.raised = False
            self.deal_community_card()
            if self.player.blind == "Big":
                self.deal_community_card()
        elif move == "call":
            self.player.callAmount(self.amountRaised)
            self.pot += self.amountRaised
            self.amountRaised = 0.00
            self.raised = False
            self.deal_community_card()
        elif move == "raise":
            self.amountRaised = amount
            self.player.raiseAmount(amount)
            self.pot += amount
            self.raised = True
            self.bot_move()
        elif move == "fold":
            self.amountRaised = 0.00
            self.raised = False
            self.player_fold(self.player)
        
    def get_winner(self):
        ai_card1 = self.ai.get_hand()[0]
        ai_card2 = self.ai.get_hand()[1]
        player_card1 = self.player.get_hand()[0]
        player_card2 = self.player.get_hand()[1]
        communityCard1 = self.communityCards[0] 
        communityCard2 = self.communityCards[1] 
        communityCard3 = self.communityCards[2] 
        communityCard1Name = communityCard1.suit + " " + communityCard1.rank 
        communityCard2Name = communityCard2.suit + " " + communityCard2.rank 
        communityCard3Name = communityCard3.suit + " " + communityCard3.rank 
        data = {
            "ai_card1": ai_card1.suit + " " + ai_card1.rank,
            "ai_card2": ai_card2.suit + " " + ai_card2.rank,
            "player_card1": player_card1.suit + " " + player_card1.rank,
            "player_card2": player_card2.suit + " " + player_card2.rank,
            "community_card1": communityCard1Name,
            "community_card2": communityCard2Name,
            "community_card3": communityCard3Name,
        }
        winner = determine_winner(data)
        if winner == "AI":
            self.player_fold(self.player)
        else:
            self.player_fold(self.ai)