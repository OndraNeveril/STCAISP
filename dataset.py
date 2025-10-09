from english_words import get_english_words_set
import random
from PIL import Image, ImageDraw, ImageFont
import os

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

def translate(text, font_path, font_size, name):
    font = ImageFont.truetype(font_path, font_size)
    img = Image.new("RGB", (1500, 300), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((20, 60), text, font=font, fill="black")

    img.save("Dataset\\zadani_"+name+".png")
    t = open("Dataset\\reseni"+name+".txt", "w")
    t.write(text)

for i in range(len(font_list)):
    f = "C:\\Users\\ondra\\dokument\\STCAIŠP\\fonty\\"+font_list[i]
    n = font_list[i][5:-9] if font_list[i] == 'sifraVelkyPolskyKrizCE-CH.ttf' else font_list[i][5:-6]
    for j in range(100):
        translate(random_paragraph(5, 3, 5), f, 20, n+"_"+str(j))
