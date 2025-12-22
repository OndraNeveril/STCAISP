from random import randint

from english_words import get_english_words_set
import random
from PIL import Image, ImageDraw, ImageFont
import os
import shutil

words = list(get_english_words_set(['web2']))

def random_sentence(word_count=random.randint(1,2)):
    selected = random.choices(words, k=word_count)
    sentence = " ".join(selected)
    return sentence.capitalize() + "."

def random_paragraph(sentence_count, min_words, max_words):
    return "\n".join(
        random_sentence(random.randint(min_words, max_words))
        for _ in range(sentence_count)
    )


# ────────────── FUNKCE PRO MEZEROVÁNÍ TEXTU ──────────────

def spaced_text(text, font_name):
    # dvě mezery pro braille / binární fonty
    if ("brail" in font_name.lower()
        or "binar" in font_name.lower()):
        sep = "  "
    elif ("semafor" in font_name.lower()
          or "posunk" in font_name.lower()):
        sep = " "  # semafor/posunky chtějí stále jednu mezeru?
    else:
        sep = " "

    output = ""
    for ch in text:
        if ch == " ":
            output += ch
        else:
            output += ch + sep

    return output.rstrip()


# ────────────── CESTY ──────────────

fonts_path = "fonty"
font_list = os.listdir(fonts_path)

base_dir = "Dataset"
train_dir = os.path.join(base_dir, "train")
test_dir = os.path.join(base_dir, "test")

if os.path.exists(base_dir):
    shutil.rmtree(base_dir)
os.makedirs(train_dir)
os.makedirs(test_dir)


# ────────────── GENERÁTOR OBRÁZKU ──────────────

def save_image(text, font_path, font_size, save_path):
    font = ImageFont.truetype(font_path, font_size)
    img = Image.new("RGB", (500, 300), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((20, 60), text, font=font, fill="black")
    img.save(save_path)


# ────────────── GENEROVÁNÍ DAT ──────────────

samples_per_class = 100
train_fraction = 0.8

for font_file in font_list:

    font_path = os.path.join(fonts_path, font_file)
    n = font_file[5:-9] if font_file == 'sifraVelkyPolskyKrizCE-CH.ttf' else font_file[5:-6]

    # určování velikosti písma podle typu fontu:
    font_lower = font_file.lower()

    if ("brail" in font_lower
        or "binar" in font_lower
        or "semafor" in font_lower
        or "posunk" in font_lower):
        font_size = 40

    elif "morse" in font_lower:
        font_size = 30

    else:
        font_size = 20

    train_class_dir = os.path.join(train_dir, n)
    test_class_dir = os.path.join(test_dir, n)
    os.makedirs(train_class_dir)
    os.makedirs(test_class_dir)

    for j in range(samples_per_class):

        raw_text = random_paragraph(randint(1, 4), 1, 1)
        text = spaced_text(raw_text, font_file)

        img_name = f"{n}_{j}.png"

        if j < samples_per_class * train_fraction:
            save_path = os.path.join(train_class_dir, img_name)
        else:
            save_path = os.path.join(test_class_dir, img_name)

        save_image(text, font_path, font_size, save_path)

print("Dataset byl úspěšně vytvořen.")