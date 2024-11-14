import torch
import pandas as pd
from torch.utils.data import DataLoader, Dataset
from model import PokerModel
from train import train_model
from evaluate import evaluate_model

# 1. Load and Preprocess the CSV Data
data = pd.read_csv("game_log.csv")

# Drop any rows with missing values
data.dropna(inplace=True)

# Prepare features and labels
# Features: All columns except the "Action" column
# Assume "Action" is added to CSV to denote what action was taken by player
X = data.drop(columns=["Action"])  # Features
y = data["Action"]  # Labels (0 for Fold, 1 for Call, 2 for Raise)

# Convert categorical labels to numeric labels if necessary
# Encoding is assumed: Fold = 0, Call = 1, Raise = 2

# Convert to PyTorch tensors
features = torch.tensor(X.values, dtype=torch.float32)
labels = torch.tensor(y.values, dtype=torch.long)  # Classification labels need to be of type `long`

# 2. Create Custom Dataset and DataLoader
class PokerDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

dataset = PokerDataset(features, labels)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)


input_size = X.shape[1]
model = PokerModel(input_size)

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001) 

# 4. Train the Model
train_model(model, train_loader, criterion, optimizer, epochs=20)

# 5. Evaluate the Model
test_input = torch.rand(1, features.shape[1])  # Example random input for evaluation
prediction = evaluate_model(model, test_input)

print(f"Predicted Action: {torch.argmax(prediction, dim=1).item()}")
