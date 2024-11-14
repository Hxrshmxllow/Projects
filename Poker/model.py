import torch
import torch.nn as nn
import torch.nn.functional as F


class PokerModel(nn.Module):
    def __init__(self, input_size):
        super(PokerModel, self, input_size).__init__()
        self.fc1 = nn.Linear(input_size, 128)  # First fully connected layer
        self.fc2 = nn.Linear(128, 128) # Hidden layer
        self.fc3 = nn.Linear(128, 3) # Output layer
    
    def forward(self, x):
        x = F.relu(self.fc1(x))  # Apply ReLU activation
        x = F.relu(self.fc2(x))
        x = self.fc3(x)              # Final output layer
        return x
    
#input:
#[Player_Card_1, Suit_1, Player_Card_2, Suit_2, Community_Cards_1, Community_Cards_2, Community_Cards_3, Community_Cards_4, Community_Cards_5, Round, Player_Stack, Pot_Size, Bet_To_Call, Player_Position, Opponent_1_Action, Hand_Strength]
#Output:
#3 actions w/ probability of win. You 


    