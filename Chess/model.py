import torch
import torch.nn as nn
import chess
from game import Game

PIECE_SYMBOLS = {
    "Pawn": {"White": "P", "Black": "p"},
    "Rook": {"White": "R", "Black": "r"},
    "Knight": {"White": "N", "Black": "n"},
    "Bishop": {"White": "B", "Black": "b"},
    "Queen": {"White": "Q", "Black": "q"},
    "King": {"White": "K", "Black": "k"},
}

def fen_to_tensor(fen):
    """Convert FEN to a 3D tensor (12x8x8)."""
    board = chess.Board(fen)  # Use python-chess to parse the FEN
    piece_map = board.piece_map()  # Get all pieces on the board

    # Initialize a tensor of zeros with shape (12, 8, 8)
    tensor = torch.zeros((12, 8, 8))

    # Map piece types to tensor channels
    piece_to_channel = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5,
    }

    for square, piece in piece_map.items():
        row, col = divmod(square, 8)  # Convert square index to row and col
        channel = piece_to_channel[piece.piece_type]
        if piece.color == chess.BLACK:  # Add 6 for black pieces
            channel += 6
        tensor[channel, row, col] = 1  # Set the tensor channel to 1

    return tensor

def index_to_move(index):
    """Convert index back to UCI move."""
    # Start and end squares from the index
    start_square = index // 64
    end_square = index % 64

    # Use python-chess to get the square names
    start_square_name = chess.SQUARE_NAMES[start_square]
    end_square_name = chess.SQUARE_NAMES[end_square]

    # Return the UCI move
    return start_square_name + end_square_name

class ChessBot(nn.Module):
    def __init__(self):
        super(ChessBot, self).__init__()
        self.conv1 = nn.Conv2d(12, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)  # New layer
        self.fc1 = nn.Linear(256 * 8 * 8, 2048)  # Adjusted dimensions
        self.fc2 = nn.Linear(2048, 1024)  # Adjusted dimensions
        self.fc3 = nn.Linear(1024, 64 * 64)  # New output layer

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Predict the best move
def predict_move(game, model_path="chess_bot.pth"):
    
    print("Loading the saved model...")
    model = ChessBot()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    print("Model loaded successfully.")

    print("Converting board to FEN format...")
    fen = convert_game_to_fen(game)
    print(f"FEN for prediction: {fen}")
    print("Predicting the best move for the given position...")
    with torch.no_grad():
        board_tensor = fen_to_tensor(fen).unsqueeze(0)
        outputs = model(board_tensor)
        best_move_index = torch.argmax(outputs).item()
        best_move = index_to_move(best_move_index)
    rows = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    start_square = best_move[:2]
    end_square = best_move[2:]
    start_row = 8 - int(start_square[1])
    start_col = rows.index(start_square[0])
    end_row = 8 - int(end_square[1])
    end_col = rows.index(end_square[0])
    return (start_row, start_col, end_row, end_col)

# Convert the custom board to FEN
def convert_game_to_fen(game):
    rows = []
    for row in game.board:  # Iterate through each row
        fen_row = ""
        empty_count = 0
        for square in row:  # Iterate through each square in the row
            piece = square.piece
            if piece is None:  # If the square is empty
                empty_count += 1
            else:
                if empty_count > 0:  # Append empty square count
                    fen_row += str(empty_count)
                    empty_count = 0
                # Get the piece symbol based on its class and color
                piece_type = type(piece).__name__  # Get the class name of the piece
                symbol = PIECE_SYMBOLS[piece_type][piece.color]
                fen_row += symbol
        if empty_count > 0:  # Add remaining empty squares
            fen_row += str(empty_count)
        rows.append(fen_row)  # Add the row to the FEN string
    fen = "/".join(rows)  # Combine all rows with '/'
    
    # Add other FEN components
    turn = "w" if game.curr_player.color == "White" else "b"
    fen += f" {turn} KQkq - 0 1"
    return fen

# Example usage
def test(fen):
    model = ChessBot()
    model.load_state_dict(torch.load("chess_bot.pth"))
    model.eval()
    print("Model loaded successfully.")

    print("Converting board to FEN format...")
    print(f"FEN for prediction: {fen}")
    print("Predicting the best move for the given position...")
    with torch.no_grad():
        board_tensor = fen_to_tensor(fen).unsqueeze(0)
        outputs = model(board_tensor)
        best_move_index = torch.argmax(outputs).item()
        best_move = index_to_move(best_move_index)
    rows = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    start_square = best_move[:2]
    end_square = best_move[2:]
    start_row = 8 - int(start_square[1])
    start_col = rows.index(start_square[0])
    end_row = 8 - int(end_square[1])
    end_col = rows.index(end_square[0])
    return (start_row, start_col, end_row, end_col)

if __name__ == "__main__":
    model = ChessBot()
    model.load_state_dict(torch.load("chess_bot.pth"))
    model.eval()
    test_fen_1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    test_fen_2 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"

    print("Test 1:")
    board_tensor_1 = fen_to_tensor(test_fen_1).unsqueeze(0)
    outputs_1 = model(board_tensor_1)
    print(f"Raw outputs for test FEN 1: {outputs_1}")

    print("Test 2:")
    board_tensor_2 = fen_to_tensor(test_fen_2).unsqueeze(0)
    outputs_2 = model(board_tensor_2)
    print(f"Raw outputs for test FEN 2: {outputs_2}")


