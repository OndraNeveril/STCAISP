from english_words import get_english_words_set
import random
from PIL import Image, ImageDraw, ImageFont
import os
import shutil

words = list(get_english_words_set(['web2']))

def random_sentence(word_count=10):
    selected = random.choices(words, k=word_count)
    sentence = " ".join(selected)
    return sentence.capitalize() + "."

def random_paragraph(sentence_count, min_words, max_words):
    return "\n".join(
        random_sentence(random.randint(min_words, max_words))
        for _ in range(sentence_count))

fonts_path = "C:\\Users\\ondra\\dokument\\STCAIŠP\\fonty"
font_list = os.listdir(fonts_path)

base_dir = "Dataset"
train_dir = os.path.join(base_dir, "train")
test_dir = os.path.join(base_dir, "test")

if os.path.exists(base_dir):
    shutil.rmtree(base_dir)
os.makedirs(train_dir)
os.makedirs(test_dir)

def save_image(text, font_path, font_size, save_path):
    font = ImageFont.truetype(font_path, font_size)
    img = Image.new("RGB", (1500, 300), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((20, 60), text, font=font, fill="black")
    img.save(save_path)

samples_per_class = 100
train_fraction = 0.8

for font_file in font_list:
    font_path = os.path.join(fonts_path, font_file)
    n = font_file[5:-9] if font_file == 'sifraVelkyPolskyKrizCE-CH.ttf' else font_file[5:-6]

    train_class_dir = os.path.join(train_dir, n)
    test_class_dir = os.path.join(test_dir, n)
    os.makedirs(train_class_dir)
    os.makedirs(test_class_dir)

    for j in range(samples_per_class):
        text = random_paragraph(5, 3, 5)
        img_name = f"{n}_{j}.png"
        if j < samples_per_class * train_fraction:
            save_image(text, font_path, 20, os.path.join(train_class_dir, img_name))
        else:
            save_image(text, font_path, 20, os.path.join(test_class_dir, img_name))

print("Dataset byl úspěšně vytvořen.")