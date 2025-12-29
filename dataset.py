from random import randint
import random
from PIL import Image, ImageDraw, ImageFont
import os
import shutil
import string
from english_words import get_english_words_set

# --- Funkce pro generování náhodných anglických textů ---
words = list(get_english_words_set(['web2']))

def random_sentence(word_count=random.randint(1,1)):
    selected = random.choices(words, k=word_count)
    sentence = " ".join(selected)
    return sentence.capitalize()

def random_paragraph(sentence_count, min_words, max_words):
    return "\n".join(random_sentence(random.randint(min_words, max_words)) for _ in range(sentence_count))

def spaced_text(text, font_name):
    sep = "  "
    output = ""
    for ch in text:
        if ch == " ":
            output += ch
        else:
            output += ch + sep
    return output.rstrip()

# --- Funkce pro vytváření obrázků z textů ---
def save_image(text, font_path, font_size, save_path, base_img_size=(100, 50), mode="text"):
    font = ImageFont.truetype(font_path, font_size)

    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    margin = 10

    if mode == "letter":
        img_width = max(base_img_size[0], text_width + 2*margin)
        img_height = max(base_img_size[1], text_height + 2*margin)

        width_variation = randint(0, 10)
        height_variation = randint(0, 5)
        img_size = (img_width + width_variation, img_height + height_variation)

        max_x_offset = img_size[0] - text_width - margin
        max_y_offset = img_size[1] - text_height - margin
        x = randint(margin, max_x_offset)
        y = randint(margin, max_y_offset)
    else:
        img_size = base_img_size
        x = 0
        y = (img_size[1] - text_height) // 2

    img = Image.new("RGB", img_size, color="white")
    draw = ImageDraw.Draw(img)
    draw.text((x, y), text, font=font, fill="black")
    img.save(save_path)

# --- Práce s adresáři ---
fonts_path = "fonty"
font_list = os.listdir(fonts_path)
dataset_texts_dir = "Dataset"
train_texts_dir = os.path.join(dataset_texts_dir, "train")
test_texts_dir = os.path.join(dataset_texts_dir, "test")

if os.path.exists(dataset_texts_dir):
    shutil.rmtree(dataset_texts_dir)
os.makedirs(train_texts_dir)
os.makedirs(test_texts_dir)

samples_per_class_text = 100
train_fraction = 0.8

dataset_letters_dir = "Dataset_letters"
samples_per_letter = 10
letter_img_size = (100, 50)
letter_font_size = 40
letters = list(string.ascii_uppercase)

if os.path.exists(dataset_letters_dir):
    shutil.rmtree(dataset_letters_dir)
os.makedirs(dataset_letters_dir)

# --- Generování datasetu šifer ---
for font_file in font_list:
    font_path = os.path.join(fonts_path, font_file)
    n = font_file[5:-9] if font_file == 'sifraVelkyPolskyKrizCE-CH.ttf' else font_file[5:-6]

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

    train_class_dir = os.path.join(train_texts_dir, n)
    test_class_dir = os.path.join(test_texts_dir, n)
    os.makedirs(train_class_dir)
    os.makedirs(test_class_dir)

    for j in range(samples_per_class_text):
        raw_text = random_paragraph(randint(1, 1), 1, 1)
        text = spaced_text(raw_text, font_file)
        img_name = f"{n}_{j}.png"
        save_path = os.path.join(train_class_dir if j < samples_per_class_text * train_fraction else test_class_dir, img_name)
        save_image(text, font_path, font_size, save_path, base_img_size=(500, 50), mode="text")
print("Dataset šifer byl úspěšně vytvořen.")

# --- Generování datasetů písmen ---
for font_file in font_list:
    font_path = os.path.join(fonts_path, font_file)
    font_name = font_file[5:-9] if font_file == 'sifraVelkyPolskyKrizCE-CH.ttf' else font_file[5:-6]

    font_dataset_dir = os.path.join(dataset_letters_dir, font_name)
    train_dir = os.path.join(font_dataset_dir, "train")
    test_dir = os.path.join(font_dataset_dir, "test")
    os.makedirs(train_dir)
    os.makedirs(test_dir)

    for letter in letters:
        os.makedirs(os.path.join(train_dir, letter))
        os.makedirs(os.path.join(test_dir, letter))

    for letter in letters:
        for j in range(samples_per_letter):
            img_name = f"{letter}_{j}.png"
            save_path = os.path.join(train_dir if j < samples_per_letter * train_fraction else test_dir,
                                     letter, img_name)
            save_image(letter, font_path, letter_font_size, save_path, base_img_size=letter_img_size, mode="letter")
print("Dataset písmen anglické abecedy byl úspěšně vytvořen. Každý font má svůj vlastní dataset se 26 třídami.")