import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Set seed 
torch.manual_seed(42)


# Inputs for all tasks: (0,0), (0,1), (1,0), (1,1)
X = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])

# Task 1-4 Labels: Binary XOR (0, 1, 1, 0)
y_binary = torch.tensor([[0.0], [1.0], [1.0], [0.0]])

# Task 5 Labels: 3-Class (0, 1, 1, 2)
y_multi = torch.tensor([0, 1, 1, 2])


class XORModel(nn.Module):
    def __init__(self, hidden_activation=nn.Sigmoid(), num_classes=1):
        super().__init__()
        # 2 inputs -> 2 hidden units
        self.hidden = nn.Linear(2, 2)
        self.activation = hidden_activation
        # 2 hidden units -> output (1 for binary, 3 for multiclass)
        self.output = nn.Linear(2, num_classes)

    def forward(self, x):
        h = self.activation(self.hidden(x))
        logits = self.output(h)
        return logits


def train_model(model, X, y, criterion, epochs=2500, lr=0.1, task='binary'):
    optimizer = optim.SGD(model.parameters(), lr=lr)
    
    initial_loss = None
    early_grad_norm = None

    for epoch in range(epochs):
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, y)
        
        if epoch == 0:
            initial_loss = loss.item()
            
        loss.backward()
        
        # Record early gradient norm at step 1
        if epoch == 1:
            early_grad_norm = torch.norm(model.hidden.weight.grad).item()
            
        optimizer.step()
        
    final_loss = loss.item()
    
    # Calculate probabilities and predictions
    with torch.no_grad():
        final_logits = model(X)
        if task == 'binary':
            probs = torch.sigmoid(final_logits)
            preds = (probs > 0.5).float()
            correct = (preds == y).all().item()
        else:
            probs = torch.softmax(final_logits, dim=1)
            preds = torch.argmax(probs, dim=1)
            correct = (preds == y).all().item()
            
    return initial_loss, final_loss, probs, preds, correct, early_grad_norm


print("--- TASK 4A: Basic Learning Check (Tanh) ---")
model_tanh = XORModel(hidden_activation=nn.Tanh(), num_classes=1)
criterion_bce = nn.BCEWithLogitsLoss()
init_loss, fin_loss, probs, preds, is_correct, _ = train_model(
    model_tanh, X, y_binary, criterion_bce, epochs=5000, lr=0.5
)
print(f"Initial Loss: {init_loss:.4f} | Final Loss: {fin_loss:.4f}")
print(f"Probabilities:\n{probs.numpy()}")
print(f"Predictions:\n{preds.numpy()}")
print(f"All Correct? {is_correct}\n")

print("--- TASK 4B & C: Symmetry Experiment (Zero Init) ---")
model_sym = XORModel(hidden_activation=nn.Tanh(), num_classes=1)
# Force weights to zero
nn.init.zeros_(model_sym.hidden.weight)
nn.init.zeros_(model_sym.hidden.bias)
nn.init.zeros_(model_sym.output.weight)
nn.init.zeros_(model_sym.output.bias)

init_loss_sym, fin_loss_sym, probs_sym, _, is_correct_sym, _ = train_model(
    model_sym, X, y_binary, criterion_bce, epochs=1000, lr=0.5
)
print("Hidden layer weights after training (Notice they remain identical):")
print(model_sym.hidden.weight.data.numpy())
print(f"All Correct? {is_correct_sym}\n")

print("--- TASK 4D: Activation Experiment ---")
activations = {
    "Sigmoid": nn.Sigmoid(),
    "Tanh": nn.Tanh(),
    "ReLU": nn.ReLU()
}
print(f"{'Activation':<10} | {'Final Loss':<10} | {'4/4 Correct?':<12} | {'Early ||grad||_2'}")
for name, act in activations.items():
    torch.manual_seed(42) # Reset seed for fair comparison
    model_act = XORModel(hidden_activation=act, num_classes=1)
    _, f_loss, _, _, corr, grad_norm = train_model(
        model_act, X, y_binary, criterion_bce, epochs=3000, lr=0.5
    )
    print(f"{name:<10} | {f_loss:<10.4f} | {str(corr):<12} | {grad_norm:.4f}")
print("\n")


print("--- TASK 5: Three-Class Decision ---")
model_multi = XORModel(hidden_activation=nn.Tanh(), num_classes=3)
criterion_ce = nn.CrossEntropyLoss()
_, fin_loss_multi, probs_multi, preds_multi, is_correct_multi, _ = train_model(
    model_multi, X, y_multi, criterion_ce, epochs=5000, lr=0.5, task='multi'
)
print("3-Class Probabilities:")
print(probs_multi.numpy())
print("3-Class Predictions:", preds_multi.numpy())
print(f"All Correct? {is_correct_multi}")

# Softmax numerical stability check (Optional diagnostic)
print("\nOptional Diagnostic (Softmax Shift Invariance):")
sample_logits = model_multi(X)[0].detach() # Take first example
probs_standard = torch.softmax(sample_logits, dim=0)
probs_shifted = torch.softmax(sample_logits + 100.0, dim=0)
print(f"Standard Softmax: {probs_standard.numpy()}")
print(f"Shifted (+100) Softmax: {probs_shifted.numpy()}")