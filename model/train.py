import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import DataLoader
from dataset import CaptchaDataset
from model import CaptchaCNN
import tqdm
from torch.utils.data import random_split
import matplotlib.pyplot as plt

epochs = 1000
batch_size = 64
learning_rate = 0.001
image_size = (60, 160)
captcha_len = 4
num_classes = 10

train_loss = []
val_accuracies = []

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([
    transforms.Resize(image_size),
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_dataset = CaptchaDataset("data/train", transform, captcha_len)
val_dataset = CaptchaDataset("data/vaild", transform, captcha_len)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
# dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

model = CaptchaCNN(num_chars=num_classes, captcha_len=captcha_len).to(device)
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss()

run_num = 1
base_foldername = "run"
foldername = "run_1"
while os.path.exists(f"outputs/{foldername}"):
    run_num += 1
    foldername = f"{base_foldername}_{run_num}"

print(foldername)

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    loop = tqdm.tqdm(train_loader, desc=f"Epoch [{epoch + 1}/{epochs}]")

    for images, labels in loop:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)

        loss = sum(criterion(outputs[:, i, :], labels[:, i]) for i in range(captcha_len))
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        preds = torch.argmax(outputs, dim=2)
        correct += (preds == labels).all(dim=1).sum().item()
        total += labels.size(0)

        loop.set_postfix(loss=loss.item())
    
    acc = correct / total
    train_loss.append(running_loss)
    print(f"Epoch {epoch + 1}/{epochs}, Train Loss: {running_loss:.4f}, Train Acc: {acc * 100:.2f}%")

    model.eval()
    val_correct = 0
    val_total = 0
    val_loop = tqdm.tqdm(val_loader, desc=f"Validating [{epoch + 1/epochs}]")
    with torch.no_grad():
        for val_images, val_labels in val_loop:
            val_images, val_labels = val_images.to(device), val_labels.to(device)
            val_outputs = model(val_images)
            val_preds = torch.argmax(val_outputs, dim=2)
            val_correct += (val_preds == val_labels).all(dim=1).sum().item()
            val_total += val_labels.size(0)
    
    val_acc = val_correct / val_total
    val_accuracies.append(val_acc)
    print(f"Validation Accuracy: {val_acc * 100:.2f}%")

    if (epoch + 1) % 100 == 0:
        os.makedirs(f"outputs/{foldername}/checkpoints", exist_ok=True)
        torch.save(model.state_dict(), f"outputs/{foldername}/checkpoints/captcha_cnn_epoch{epoch + 1}.pth")

# os.makedirs("checkpoints", exist_ok=True)
torch.save(model.state_dict(), f"outputs/{foldername}/captcha_cnn.pth")

plt.figure(figsize=(10, 5))
plt.plot(train_loss, label="Train Loss")
plt.plot([v * 100 for v in val_accuracies], label="Val Accuracy (%)")
plt.xlabel("Epoch")
plt.ylabel("Value")
plt.legend()
plt.title(f"Training Progress - Epoch {epoch + 1}")
plt.grid(True)
os.makedirs("outputs", exist_ok=True)
plt.savefig(f"outputs/{foldername}/training_plot_epoch{epoch + 1}.png")
plt.close()