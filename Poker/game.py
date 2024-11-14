import random
import csv
from collections import Counter
from treys import Card as TreysCard, Evaluator
import openai
import os

openai.api_key = ''

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
        self.game_log = []
        self.prompt = ""

    def resetDeck(self):
        self.communityCards = []
        for player in self.players:
            player.hand = []
        self.deck = [Card(suit, rank, Poker.ranks.index(rank) + 1) for suit in Poker.suits for rank in Poker.ranks]
    
    def log_game_state(self):
        suit_mapping = {"Spade": 1, "Heart": 2, "Club": 3, "Diamond": 4}
        rank_mapping = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14
        }
        round_mapping = {"Pre-Flop": 0, "Flop": 1, "Turn": 2, "River": 3}
        action_mapping = {"Fold": 0, "Call": 1, "Raise": 2, "N/A": -1}

        for i, player in enumerate(self.players):
            player_hand = player.hand
            player_card_1 = player_hand[0] if len(player_hand) > 0 else None
            player_card_2 = player_hand[1] if len(player_hand) > 1 else None

            community_cards = [None] * 5 
            for j in range(len(self.communityCards)):
                community_cards[j] = self.communityCards[j]

            player_card_1_value = rank_mapping.get(str(player_card_1.rank), 0) if player_card_1 else 0
            player_card_1_suit = suit_mapping.get(player_card_1.suit, 0) if player_card_1 else 0

            player_card_2_value = rank_mapping.get(str(player_card_2.rank), 0) if player_card_2 else 0
            player_card_2_suit = suit_mapping.get(player_card_2.suit, 0) if player_card_2 else 0

            community_card_values_flat = []
            for card in community_cards:
                rank = rank_mapping.get(str(card.rank), 0) if card else 0
                suit = suit_mapping.get(card.suit, 0) if card else 0
                community_card_values_flat.extend([rank, suit])

            round_value = round_mapping.get(self.round, -1)

            player_stack = player.money

            pot_size = self.pot

            bet_to_call = self.raiseAmount

            player_position = i 

            opponent_action = action_mapping.get("N/A", -1)

            hand_strength = self.evaluate_player_hand(player)

            game_data = [
                player_card_1_value, player_card_1_suit,
                player_card_2_value, player_card_2_suit,
                *community_card_values_flat,
                round_value,
                player_stack,
                pot_size,
                bet_to_call,
                player_position,
                opponent_action,
                hand_strength
            ]

            self.game_log.append(game_data)

    def evaluate_player_hand(self, player):
        evaluator = Evaluator()

        # Convert player hand to Treys Card format
        player_hand = []
        try:
            for card in player.hand:
                # Convert rank to the correct representation for Treys
                if isinstance(card.rank, int):
                    if card.rank == 10:
                        rank = 'T'
                    else:
                        rank = str(card.rank)
                else:
                    rank = card.rank[0].upper()  # Ensure rank for face cards is properly formatted (J, Q, K, A)
                suit = card.suit[0].lower()  # Convert suit to lowercase

                # Create the Treys card and add it to player_hand
                player_hand.append(TreysCard.new(f"{rank}{suit}"))
        except Exception as e:
            print(f"Error converting player hand: {e}")
            return -1  # Return -1 to indicate an error in hand conversion

        # Convert community cards to Treys Card format
        board = []
        try:
            for card in self.communityCards:
                if card is not None:
                    # Convert rank and suit for community cards
                    if isinstance(card.rank, int):
                        if card.rank == 10:
                            rank = 'T'
                        else:
                            rank = str(card.rank)
                    else:
                        rank = card.rank[0].upper()
                    suit = card.suit[0].lower()

                    # Create the Treys card and add it to the board
                    board.append(TreysCard.new(f"{rank}{suit}"))
        except Exception as e:
            print(f"Error converting community cards: {e}")
            return -1  # Return -1 to indicate an error in community card conversion

        # Add unique dummy cards if fewer than 5 community cards are available
        dummy_cards = ['2c', '3d', '4h', '5s', '6c']  # List of dummy cards
        dummy_index = 0
        while len(board) < 5:
            board.append(TreysCard.new(dummy_cards[dummy_index]))
            dummy_index += 1

        # Evaluate the player's hand strength
        try:
            if len(board) + len(player_hand) == 7:
                hand_strength = evaluator.evaluate(board, player_hand)
            else:
                print("Error: Not enough cards for evaluation.")
                return -1
        except KeyError as e:
            print(f"Error during evaluation: {e}")
            return -1  # Return -1 to indicate an evaluation error

        return hand_strength
    
    def get_gpt_action(self, gamePrompt):
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a poker player deciding whether to raise, call, or fold."},
            {"role": "user", "content": gamePrompt}
        ],
        max_tokens=50,
        temperature=0.7
        )
        decision = response['choices'][0]['message']['content'].strip()
        if "raise" in decision.lower():
            return 1
        elif "call" in decision.lower():
            return 2
        elif "fold" in decision.lower():
            return 3
        else:
            return 3
    
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
                self.prompt = f"Pot: ${self.pot} Your Money: ${player.money} and Cards: "
                for card in player.hand:
                    self.prompt += f"{card.suit} {card.rank} "
                self.prompt += "\n"
                if player != playerRaised:
                    options = {1: "Raise", 2: f"Call ${self.raiseAmount}", 3: "Fold"}
                    for option in options:
                        self.prompt += f"{option}. {options[option]}" #chatgpt
                        print(f"{option}. {options[option]}")
                    self.prompt += "What would you do here?" #chatgpt
                    #choice = int(input(f"What would {player.name} like to do? "))
                    choice = int(self.get_gpt_action(self.prompt))
                    print(f"{player.name} has chosen to {options[choice]}.")
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
                self.prompt = f"Pot: ${self.pot} Your Money: ${player.money} and Cards: "
                for card in player.hand:
                    self.prompt += f"{card.suit} {card.rank} "
                self.prompt += "\n"
                options = {1: "Raise", 2: "Check", 3: "Fold"}
                if self.potRaised:
                    options[2] = f"Call ${self.raiseAmount}"
                for option in options:
                    self.prompt += f"{option}. {options[option]}" #chatgpt
                    print(f"{option}. {options[option]}")
                self.prompt += "What would you do here?" #chatgpt
                #choice = int(input(f"What would {player.name} like to do? "))
                choice = int(self.get_gpt_action(self.prompt))
                print(f"{player.name} has chosen to {options[choice]}.")
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
        self.log_game_state()
        return self.bet(False, None)
    
    def flop(self):
        self.round = "Flop"
        for i in range(3):
            card = random.choice(self.deck)
            self.communityCards.append(card)
            self.deck.remove(card)
        self.printGame()
        self.log_game_state()
        return self.bet(False, None)
    
    def turn(self):
        self.round = "Turn"
        card = random.choice(self.deck)
        self.communityCards.append(card)
        self.deck.remove(card)
        self.printGame()
        self.log_game_state()
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
        
    def save_game_log_to_csv(self, filename="game_log.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Player_Card_1", "Suit_1",
                "Player_Card_2", "Suit_2",
                "Community_Cards_1", "Community_Suit_1",
                "Community_Cards_2", "Community_Suit_2",
                "Community_Cards_3", "Community_Suit_3",
                "Community_Cards_4", "Community_Suit_4",
                "Community_Cards_5", "Community_Suit_5",
                "Round", "Player_Stack", "Pot_Size", "Bet_To_Call",
                "Player_Position", "Opponent_1_Action", "Hand_Strength"
            ])
            for entry in self.game_log:
                writer.writerow(entry)
        print(f"Game log saved to {filename}")
    
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
    try:
        while run and 0 not in [player.money for player in game.players]:
            if game.preFlop() is False:
                if game.flop() is False:
                    if game.turn() is False:
                        game.river()
    except KeyboardInterrupt:
        print("\nGame ended by user.")
    game.save_game_log_to_csv()

if __name__ == "__main__":
    main()