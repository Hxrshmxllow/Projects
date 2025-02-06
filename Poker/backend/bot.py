from openai import OpenAI
import os


client = OpenAI(api_key="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")

def get_ai_move(data):
    if data["call_amount"] == 0:
        check = 'Check,'
    else:
        check = ""
    prompt = f"""
    You are an expert poker AI making decisions based on the current game state. 
    Choose the best move: {check} Call {data["call_amount"]}, Raise (give amount), or Fold.

    Current Game State:
    - AI Cards: {data["ai_card1"]}, {data["ai_card2"]}
    - Pot: ${data["pot"]}
    - Round: {data["round"]}
    - Community Cards: {data["community_card1"]}, {data["community_card2"]}, {data["community_card3"]}
    - AI Money: ${data["ai_money"]}

    Choose the best move for the AI:
    """
    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[{"role": "system", "content": "You are a poker AI deciding the best move."},
                  {"role": "user", "content": prompt}],
        max_tokens=50)
        ai_move = response.choices[0].message.content.strip()
        return ai_move
    except Exception as e:
        print("Error calling OpenAI API:", e)
        return "Check" 

def determine_winner(data):
    prompt = f"""
    You are a poker referee following official Texas Hold'em rules.  
    Your task is to determine the winner of a poker hand based on the best 5-card combination.  
    Return only one word: "AI" if AI wins, or "Player" if the player wins. No extra text.

    ###Rules to Follow:
    1. The best 5-card hand must be selected from each player's two hole cards and five community cards.
    2. Hand rankings follow official Texas Hold'em rules:
    - Royal Flush > Straight Flush > Four of a Kind > Full House > Flush > Straight > Three of a Kind > Two Pair > One Pair > High Card.
    3. If both players have the same hand rank, determine the winner based on the highest kicker.
    4. Do not assume missing cards. Only evaluate based on the given data.


    ###Current Game State:
    - AI Cards: {data["ai_card1"]}, {data["ai_card2"]}
    - Player Cards: {data["player_card1"]}, {data["player_card2"]}
    - Community Cards: {data["community_card1"]}, {data["community_card2"]}, {data["community_card3"]}

    Now, determine the winner by following the rules above and return only one word: "AI" or "Player".
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a poker referee following official Texas Hold'em rules."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,  
        )
        ai_response = response.choices[0].message.content.strip()
        print(ai_response)
        return ai_response
    except Exception as e:
        print("Error calling OpenAI API:", e)
        return "Error"

