import os
import time
import math
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from tkinter import Label
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

# ────────────── KONSTANTY ──────────────
LETTER_SIZE = (80, 50)   # (W, H) – PIL
TORCH_SIZE  = (50, 80)   # (H, W) – torchvision

device = "cuda" if torch.cuda.is_available() else "cpu"

# ────────────── UTIL ──────────────
def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def accuracy_fn(y_true, y_pred):
    y_pred_class = torch.argmax(y_pred, dim=1)
    correct = torch.eq(y_true, y_pred_class).sum().item()
    return (correct / len(y_pred)) * 100

# ────────────── DATASET ──────────────
class CustomDataset(Dataset):
    def __init__(self, root_folder, img_size=TORCH_SIZE):
        self.images = []
        self.labels = []
        self.classes = []

        for class_name in sorted(os.listdir(root_folder)):
            class_path = os.path.join(root_folder, class_name)
            if not os.path.isdir(class_path):
                continue
            self.classes.append(class_name)
            for root, _, files in os.walk(class_path):
                for file in files:
                    if file.endswith(".png"):
                        self.images.append(os.path.join(root, file))
                        self.labels.append(self.classes.index(class_name))

        self.transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize(img_size),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img = Image.open(self.images[idx])
        img = self.transform(img)
        return img, self.labels[idx]

# ────────────── MODEL ──────────────
def create_model(num_classes):
    return nn.Sequential(
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
        nn.Dropout(0.1),
        nn.Linear(128, num_classes)
    ).to(device)

def train_model(train_dataset, test_dataset, save_path, n_epochs=20, batch_size=16, learning_rate=3e-4):
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader  = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    num_classes = len(train_dataset.classes)
    model = create_model(num_classes)

    optimizer = optim.AdamW(model.parameters(), lr=learning_rate)
    loss_fn = nn.CrossEntropyLoss()

    best_test_acc = 0
    start_time = time.time()

    for epoch in range(n_epochs):
        model.train()
        train_losses, train_accs = [], []

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

        model.eval()
        test_losses, test_accs = [], []
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

        print(
            f"{timeSince(start_time)} | Epoch {epoch+1}/{n_epochs} | "
            f"Train loss: {avg_train_loss:.5f}, acc: {avg_train_acc:.2f}% | "
            f"Test loss: {avg_test_loss:.5f}, acc: {avg_test_acc:.2f}%"
        )

        if avg_test_acc > best_test_acc:
            best_test_acc = avg_test_acc
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            torch.save(model.state_dict(), save_path)

def trenovani_vse():
    os.makedirs("modely", exist_ok=True)

    # ───── HLAVNÍ MODEL – ROZPOZNÁNÍ ŠIFRY ─────
    train_dataset = CustomDataset("Dataset/train", img_size=(128, 512))
    test_dataset  = CustomDataset("Dataset/test",  img_size=(128, 512))

    print("Trénuji hlavní model na Dataset...")
    """train_model(
        train_dataset,
        test_dataset,
        save_path=os.path.join("modely", "best_model.pth"),
        n_epochs=20,
        batch_size=16,
        learning_rate=3e-4
    )"""

    # ───── MODELY PRO JEDNOTLIVÉ ŠIFRY (PÍSMENA) ─────
    letters_dir = "Dataset_letters"

    for sifra_typ in sorted(os.listdir(letters_dir)):
        sifra_path = os.path.join(letters_dir, sifra_typ)
        if not os.path.isdir(sifra_path):
            continue

        print(f"Trénuji model pro šifru: {sifra_typ}")

        train_dataset = CustomDataset(
            os.path.join(sifra_path, "train"),
            img_size=(80, 50)
        )
        test_dataset = CustomDataset(
            os.path.join(sifra_path, "test"),
            img_size=(80, 50)
        )

        model_save_path = os.path.join("modely", f"{sifra_typ}_model.pth")

        train_model(
            train_dataset,
            test_dataset,
            save_path=model_save_path,
            n_epochs=20,
            batch_size=8,
            learning_rate=8e-4  # nižší LR, aby se písmena lépe naučila
        )


def rozpoznat(t, img, font_model_path=None):
    """
    Rozpozná typ šifry (A01, Morse, …) z celého obrázku
    """
    if img is None:
        t.config(text="Nezvolen žádný obrázek")
        return

    classes = [
        "A01", "AZ", "BinarniCtverce", "BrailovoPismo",
        "Mobil", "Morse", "PosunkovaAbeceda",
        "Semafor", "VelkyPolskyKriz", "Zlomky"
    ]

    num_classes = len(classes)
    model = create_model(num_classes)

    model_path = font_model_path or os.path.join("modely", "best_model.pth")
    if not os.path.exists(model_path):
        t.config(text="Model nebyl nalezen. Nejprve ho natrénujte.")
        return

    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((128, 512)),
        transforms.ToTensor()
    ])

    img_tensor = transform(img).unsqueeze(0).to(device)

    with torch.inference_mode():
        y_pred = model(img_tensor)
        pred_class = torch.argmax(y_pred, dim=1).item()

    t.config(text=f"Šifra rozpoznána: {classes[pred_class]}")

# ────────────── NORMALIZACE ZNAKU ──────────────
def normalize_znak(znak_img):
    znak_img = znak_img.convert("L")

    bbox = znak_img.getbbox()
    if bbox:
        znak_img = znak_img.crop(bbox)

    w, h = znak_img.size
    tw, th = LETTER_SIZE

    scale = min((tw - 4) / w, (th - 4) / h)
    new_w, new_h = int(w * scale), int(h * scale)

    znak_img = znak_img.resize((new_w, new_h), Image.BILINEAR)

    canvas = Image.new("L", LETTER_SIZE, 255)
    x = (tw - new_w) // 2
    y = (th - new_h) // 2
    canvas.paste(znak_img, (x, y))

    return canvas

# ────────────── EXTRAKCE ZNAKŮ ──────────────
def extrahovat_znaky(img, sifra_typ, vizualizace=True, padding=2, min_znak_sirka=5):
    img_gray = img.convert("L")
    img_bw = img_gray
    width, height = img_bw.size

    řádky = []
    in_line = False
    start_y = 0

    for y in range(height):
        row = [img_bw.getpixel((x, y)) for x in range(width)]
        if any(p < 200 for p in row) and not in_line:
            in_line = True
            start_y = max(0, y - padding)
        elif all(p > 200 for p in row) and in_line:
            řádky.append((start_y, min(height, y + padding)))
            in_line = False

    if in_line:
        řádky.append((start_y, height))

    znaky = []
    for y1, y2 in řádky:
        x = 0
        while x < width:
            while x < width and all(img_bw.getpixel((x, y)) > 200 for y in range(y1, y2)):
                x += 1
            if x >= width:
                break

            start_x = max(0, x - padding)
            end_x = x
            while end_x < width:
                col = [img_bw.getpixel((end_x, y)) for y in range(y1, y2)]
                if all(p > 200 for p in col):
                    gap = 0
                    while end_x + gap < width and all(
                        img_bw.getpixel((end_x + gap, y)) > 200 for y in range(y1, y2)
                    ):
                        gap += 1
                    if gap >= min_znak_sirka:
                        break
                    end_x += gap
                end_x += 1

            znak = img_bw.crop((start_x, y1, min(width, end_x + padding), y2))
            znaky.append(znak)
            x = end_x

    if vizualizace:
        os.makedirs("znaky_vizualizace", exist_ok=True)
        for i, z in enumerate(znaky):
            z.save(f"znaky_vizualizace/{sifra_typ}_{i}.png")

    return znaky

# ────────────── ŘEŠENÍ ──────────────
def vyresit(t, img=None, rozpoznano_label=None):
    if img is None:
        t.config(text="Nezvolen žádný obrázek")
        return

    if rozpoznano_label is None or "Šifra rozpoznána:" not in rozpoznano_label.cget("text"):
        t.config(text="Nejprve rozpoznej šifru")
        return

    sifra_typ = rozpoznano_label.cget("text").replace("Šifra rozpoznána: ", "")
    znaky = extrahovat_znaky(img, sifra_typ)

    model_path = f"modely/{sifra_typ}_model.pth"
    dataset_path = f"Dataset_letters/{sifra_typ}/train"

    if not os.path.exists(model_path) or not os.path.exists(dataset_path):
        t.config(text="Chybí model nebo dataset")
        return

    dataset = CustomDataset(dataset_path)
    classes = dataset.classes

    model = create_model(len(classes))
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize(TORCH_SIZE),
        transforms.ToTensor()
    ])

    vysledek = ""
    with torch.inference_mode():
        for znak in znaky:
            znak = normalize_znak(znak)
            tensor = transform(znak).unsqueeze(0).to(device)
            pred = model(tensor)
            vysledek += classes[torch.argmax(pred, 1).item()]

    t.config(text=f"Šifra vyřešena:\n{vysledek}")

def vstup():
    """Vybere vstupní soubor a vrátí PIL.Image objekt"""
    file_path = askopenfilename()
    if file_path:
        img = Image.open(file_path)
        return img
    return None

if __name__ == "__main__":
    # Spustí se jen při přímém spuštění - za účelem trénování
    print("Spouštím trénování všech modelů...")
    trenovani_vse()