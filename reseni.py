from tkinter import Label
from tkinter.filedialog import askopenfilename
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import time
import math
from torchvision import datasets, transforms
from torch.utils.data import Dataset, DataLoader, random_split
from PIL import Image
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
 	
def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def accuracy_fn(y_true, y_pred):
    y_pred_class = torch.argmax(y_pred, dim=1)
    correct = torch.eq(y_true, y_pred_class).sum().item()
    acc = (correct / len(y_pred)) * 100
    return acc

class CustomDataset(Dataset):
    def __init__(self, root_folder):
        self.images = []
        self.labels = []
        self.classes = []

        # projdi všechny složky uvnitř root_folder
        for class_name in sorted(os.listdir(root_folder)):
            class_path = os.path.join(root_folder, class_name)
            if not os.path.isdir(class_path):
                continue
            self.classes.append(class_name)
            # projdi všechny soubory v této složce
            for root, _, files in os.walk(class_path):  # <-- rekurzivně
                for file in files:
                    if file.endswith(".png"):
                        self.images.append(os.path.join(root, file))
                        self.labels.append(self.classes.index(class_name))

        print(f"Načteno {len(self.images)} obrázků, třídy: {self.classes}")

        self.transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((128, 512)),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img = Image.open(self.images[idx])
        img = self.transform(img)
        label = self.labels[idx]
        return img, label

def trenovani_vlastni_dataset():
    # --- Načtení datasetu ---
    train_dataset = CustomDataset("dataset/train")
    test_dataset  = CustomDataset("dataset/test")

    print(f"Train size: {len(train_dataset)}, Test size: {len(test_dataset)}, Classes: {train_dataset.classes}")

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    test_loader  = DataLoader(test_dataset, batch_size=16, shuffle=False)

    num_classes = len(train_dataset.classes)

    # --- Model ---
    model = nn.Sequential(
        nn.Conv2d(1, 16, 3, padding=1),
        nn.BatchNorm2d(16),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1),
        nn.BatchNorm2d(32),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.AdaptiveAvgPool2d((8, 8)),
        nn.Flatten(),
        nn.Linear(32 * 8 * 8, 128),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(128, num_classes)
    ).to(device)

    print(model)

    optimizer = optim.AdamW(model.parameters(), lr=5e-4)
    loss_fn = nn.CrossEntropyLoss()

    n_epochs = 20
    start_time = time.time()
    best_test_acc = 0

    for epoch in range(n_epochs):
        # --- Training ---
        model.train()
        train_losses = []
        train_accs = []
        for Xbatch, ybatch in train_loader:
            Xbatch, ybatch = Xbatch.to(device), ybatch.to(device)
            y_pred = model(Xbatch)
            loss = loss_fn(y_pred, ybatch)
            acc = accuracy_fn(ybatch, y_pred)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_losses.append(loss.item())
            train_accs.append(acc)

        # --- Evaluation ---
        model.eval()
        test_losses = []
        test_accs = []
        with torch.inference_mode():
            for Xtest, ytest in test_loader:
                Xtest, ytest = Xtest.to(device), ytest.to(device)
                y_pred = model(Xtest)
                test_loss = loss_fn(y_pred, ytest)
                test_acc = accuracy_fn(ytest, y_pred)
                test_losses.append(test_loss.item())
                test_accs.append(test_acc)

        avg_train_loss = np.mean(train_losses)
        avg_train_acc  = np.mean(train_accs)
        avg_test_loss  = np.mean(test_losses)
        avg_test_acc   = np.mean(test_accs)

        print(f"{timeSince(start_time)} | Epoch: {epoch+1}/{n_epochs} | "
              f"Train loss: {avg_train_loss:.5f}, acc: {avg_train_acc:.2f}% | "
              f"Test loss: {avg_test_loss:.5f}, acc: {avg_test_acc:.2f}%")

        # --- Uložení nejlepšího modelu ---
        if avg_test_acc > best_test_acc:
            best_test_acc = avg_test_acc
            torch.save(model.state_dict(), "best_model.pth")


trenovani_vlastni_dataset()
input()

def rozpoznat(t):
    t.config(text = "Šifra rozpoznána")

def vyresit(t):
    t.config(text = "Šifra vyřešena")

def vstup(input_file, root):
    """Vybere vstupní soubor a zobrazí ho"""
    if input_file == None:
        input_file = askopenfilename()
        img = Image.open(input_file)
        display = ImageTk.PhotoImage(img)
        label = Label(root, image=display, bg="white")
        label.image = display
        label.pack()
        return input_file
