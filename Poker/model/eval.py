from treys import Card, Evaluator

evaluator = Evaluator()
board = [Card.new('Th'), Card.new('Js'), Card.new('Qc')]  # Community cards (Ten of Hearts, Jack of Spades, Queen of Clubs)
hand = [Card.new('Kh'), Card.new('Ah')]  # Player's hole cards (King of Hearts, Ace of Hearts)

hand_strength = evaluator.evaluate(board, hand)
print(f"Hand Strength Score: {hand_strength}")
