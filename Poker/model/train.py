import torch 

def train_model(model, train_loader, criterion, optimizer, epochs=20):
    for epoch in range(epochs):
        model.train()  # Set the model to training mode
        running_loss = 0.0
        for features, labels in train_loader:
            optimizer.zero_grad()  # Zero the gradients
            predictions = model(features)  # Forward pass
            loss = criterion(predictions, labels)  # Compute the loss
            loss.backward()  # Backward pass
            optimizer.step()  # Update weights
            running_loss += loss.item()  # Accumulate the loss
        
        print(f"Epoch {epoch + 1}, Loss: {running_loss / len(train_loader)}")