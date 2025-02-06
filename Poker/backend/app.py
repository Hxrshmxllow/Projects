from flask import Flask, jsonify, request
from flask_cors import CORS
from game import Game

app = Flask(__name__)
CORS(app)
game = Game()

@app.route('/')
def home():
    global game
    return jsonify(
        {
            "player_card1": None,
            "player_card2": None,
            "ai_card1": None,
            "ai_card2": None,
            "pot": game.pot,
            "round": game.round,
            "community_card1": None,
            "community_card2": None,
            "community_card3": None,
            "player_money": game.player.money,
            "ai_money": game.ai.money
        }
    )  

@app.route("/pre-flop", methods=["GET", "POST"])
def pre_flop():
    global game
    if request.method == "GET":
        game.pre_flop()
        player_hand = game.player.get_hand()
        ai_hand = game.ai.get_hand()
        return jsonify(
            {
                "player_card1": player_hand[0].get_img(),
                "player_card2": player_hand[1].get_img(),
                "ai_card1": ai_hand[0].get_img(),
                "ai_card2": ai_hand[1].get_img(),
                "pot": game.pot,
                "round": game.round,
                "community_card1": None,
                "community_card2": None,
                "community_card3": None,
                "player_money": game.player.money,
                "ai_money": game.ai.money,
                "raised": game.raised,
                "amount_raised": game.amountRaised,
                "winner": game.winner,
                "aiMove": game.ai.move
            }
        )
    elif request.method == "POST":
        try:
            data = request.get_json()
            move = data["move"]
            amount = data["amount"]
            game.player_move(move, amount)
            player_hand = game.player.get_hand()
            ai_hand = game.ai.get_hand()
            community_cards = game.communityCards if len(game.communityCards) > 0 else None
            game.round = "Flop"
            return jsonify(
                {
                    "player_card1": player_hand[0].get_img(),
                    "player_card2": player_hand[1].get_img(),
                    "ai_card1": ai_hand[0].get_img(),
                    "ai_card2": ai_hand[1].get_img(),
                    "pot": game.pot,
                    "round": game.round,
                    "community_card1": community_cards[0].get_img() if community_cards else None,
                    "community_card2": None,
                    "community_card3": None,
                    "player_money": game.player.money,
                    "ai_money": game.ai.money,
                    "raised": game.raised,
                    "amount_raised": game.amountRaised,
                    "winner": game.winner,
                    "aiMove": game.ai.move
                }
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/flop", methods=["GET", "POST"])
def flop():
    global game
    if request.method == "GET":
        game.flop()
        player_hand = game.player.get_hand()
        ai_hand = game.ai.get_hand()
        community_cards = game.communityCards if len(game.communityCards) > 0 else None
        return jsonify(
            {
                "player_card1": player_hand[0].get_img(),
                "player_card2": player_hand[1].get_img(),
                "ai_card1": ai_hand[0].get_img(),
                "ai_card2": ai_hand[1].get_img(),
                "pot": game.pot,
                "round": game.round,
                "community_card1": community_cards[0].get_img() if community_cards else None,
                "community_card2": None,
                "community_card3": None,
                "player_money": game.player.money,
                "ai_money": game.ai.money,
                "raised": game.raised,
                "amount_raised": game.amountRaised,
                "winner": game.winner,
                "aiMove": game.ai.move
            }
        )
    elif request.method == "POST":
        try:
            data = request.get_json()
            move = data["move"]
            amount = data["amount"]
            game.player_move(move, amount)
            player_hand = game.player.get_hand()
            ai_hand = game.ai.get_hand()
            community_cards = game.communityCards if len(game.communityCards) > 0 else None
            game.round = "River"
            return jsonify(
                {
                    "player_card1": player_hand[0].get_img(),
                    "player_card2": player_hand[1].get_img(),
                    "ai_card1": ai_hand[0].get_img(),
                    "ai_card2": ai_hand[1].get_img(),
                    "pot": game.pot,
                    "round": game.round,
                    "community_card1": community_cards[0].get_img() if community_cards else None,
                    "community_card2": community_cards[1].get_img() if community_cards else None,
                    "community_card3": None,
                    "player_money": game.player.money,
                    "ai_money": game.ai.money,
                    "raised": game.raised,
                    "amount_raised": game.amountRaised,
                    "winner": game.winner,
                    "aiMove": game.ai.move
                }
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
@app.route("/turn", methods=["GET", "POST"])
def turn():
    global game
    if request.method == "GET":
        game.river()
        player_hand = game.player.get_hand()
        ai_hand = game.ai.get_hand()
        community_cards = game.communityCards if len(game.communityCards) > 0 else None
        return jsonify(
            {
                "player_card1": player_hand[0].get_img(),
                "player_card2": player_hand[1].get_img(),
                "ai_card1": ai_hand[0].get_img(),
                "ai_card2": ai_hand[1].get_img(),
                "pot": game.pot,
                "round": game.round,
                "community_card1": community_cards[0].get_img() if community_cards else None,
                "community_card2": community_cards[1].get_img() if community_cards else None,
                "community_card3": None,
                "player_money": game.player.money,
                "ai_money": game.ai.money,
                "raised": game.raised,
                "amount_raised": game.amountRaised,
                "winner": game.winner,
                "aiMove": game.ai.move
            }
        )
    elif request.method == "POST":
        try:
            data = request.get_json()
            move = data["move"]
            amount = data["amount"]
            game.player_move(move, amount)
            player_hand = game.player.get_hand()
            ai_hand = game.ai.get_hand()
            community_cards = game.communityCards if len(game.communityCards) > 0 else None
            game.round = "River"
            return jsonify(
                {
                    "player_card1": player_hand[0].get_img(),
                    "player_card2": player_hand[1].get_img(),
                    "ai_card1": ai_hand[0].get_img(),
                    "ai_card2": ai_hand[1].get_img(),
                    "pot": game.pot,
                    "round": game.round,
                    "community_card1": community_cards[0].get_img() if community_cards else None,
                    "community_card2": community_cards[1].get_img() if community_cards else None,
                    "community_card3": community_cards[2].get_img() if community_cards else None,
                    "player_money": game.player.money,
                    "ai_money": game.ai.money,
                    "raised": game.raised,
                    "amount_raised": game.amountRaised,
                    "winner": game.winner,
                    "aiMove": game.ai.move
                }
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
@app.route("/river", methods=["GET", "POST"])
def river():
    global game
    if request.method == "GET":
        game.river()
        player_hand = game.player.get_hand()
        ai_hand = game.ai.get_hand()
        community_cards = game.communityCards if len(game.communityCards) > 0 else None
        return jsonify(
            {
                "player_card1": player_hand[0].get_img(),
                "player_card2": player_hand[1].get_img(),
                "ai_card1": ai_hand[0].get_img(),
                "ai_card2": ai_hand[1].get_img(),
                "pot": game.pot,
                "round": game.round,
                "community_card1": community_cards[0].get_img() if community_cards else None,
                "community_card2": community_cards[1].get_img() if community_cards else None,
                "community_card3": community_cards[2].get_img() if community_cards else None,
                "player_money": game.player.money,
                "ai_money": game.ai.money,
                "raised": game.raised,
                "amount_raised": game.amountRaised,
                "winner": game.winner,
                "aiMove": game.ai.move
            }
        )
    elif request.method == "POST":
        try:
            data = request.get_json()
            move = data["move"]
            amount = data["amount"]
            game.player_move(move, amount)
            game.get_winner()
            player_hand = game.player.get_hand()
            ai_hand = game.ai.get_hand()
            community_cards = game.communityCards if len(game.communityCards) > 0 else None
            game.round = "River"
            return jsonify(
                {
                    "player_card1": player_hand[0].get_img(),
                    "player_card2": player_hand[1].get_img(),
                    "ai_card1": ai_hand[0].get_img(),
                    "ai_card2": ai_hand[1].get_img(),
                    "pot": game.pot,
                    "round": game.round,
                    "community_card1": community_cards[0].get_img() if community_cards else None,
                    "community_card2": community_cards[1].get_img() if community_cards else None,
                    "community_card3": community_cards[2].get_img() if community_cards else None,
                    "player_money": game.player.money,
                    "ai_money": game.ai.money,
                    "raised": game.raised,
                    "amount_raised": game.amountRaised,
                    "winner": game.winner,
                    "aiMove": game.ai.move
                }
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    
if __name__ == '__main__':
    app.run()