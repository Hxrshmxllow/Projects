import torch

def evaluate_model(model, test_input):
    model.eval()
    with torch.no_grad():
        prediction = model(test_input)
        return prediction