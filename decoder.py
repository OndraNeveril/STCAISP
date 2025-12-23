from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import reseni

img = None
img_label = None

root = Tk()
root.title("Decoder")
root.configure(background="white")
root.attributes("-fullscreen", False)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame_start = Frame(root)
frame_decode = Frame(root)
frame_encode = Frame(root)

for frame in (frame_start, frame_decode, frame_encode):
    frame.grid(row=0, column=0, sticky='nsew')
    frame.configure(background="white")

def show_frame(frame):
    frame.tkraise()

#Výběr souboru
def vyber_soubor():
    global img, img_label
    img = reseni.vstup()
    if img_label is not None:
        img_label.destroy()
        img_label = None
        t1.config(text=f"Šifra nerozpoznána")
        t2.config(text=f"Šifra nevyřešena")
    if img:
        display = ImageTk.PhotoImage(img)
        img_label = Label(frame_decode, image=display, bg="white")
        img_label.image = display
        img_label.pack()


def spaced_text(text, font_name):
    font_lower = font_name.lower()
    sep = "  "
    output = ""
    for ch in text:
        if ch == " ":
            output += ch
        else:
            output += ch + sep
    return output.rstrip()

# --- Zašifrování textu ---
def Take_input(font):
    if font is None:
        t3.config(text="Šifra nevybrána!", background="white", font=("Font", 20), fg="red")
        t3.pack(pady=30)
    else:
        raw_text = inputtxt.get("1.0", "end-1c")
        font_lower = font.lower()
        if "brail" in font_lower or "binar" in font_lower or "semafor" in font_lower or "posunk" in font_lower:
            font_size = 40
        elif "morse" in font_lower:
            font_size = 30
        else:
            font_size = 20
        text = spaced_text(raw_text, font)
        font_obj = ImageFont.truetype(f"fonty/{font}", font_size)
        img_width, img_height = 500, 50
        img = Image.new("RGB", (img_width, img_height), color="white")
        draw = ImageDraw.Draw(img)
        bbox = font_obj.getbbox(text)  # vrací (x0, y0, x1, y1)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        y = (img_height - text_height) // 2
        draw.text((0, y), text, font=font_obj, fill="black")
        img.save("output/sifra.png")
        t3.config(text="Šifra zašifrována,\nsoubor uložen do složky output", background="white", font=("Font", 20),
                  fg="green")
        t3.pack(pady=30)
        inputtxt.delete("1.0", "end")
        vyber.set("Vyber druh šifry")

#Výběr šifry
vybrany_font = None
def potvrdit():
    global vybrany_font
    vybrany_font = vyber.get()

# --- Startovací okno ---
Button(frame_start, text="Zašifrovat text", font=("Font", 20), command=lambda: show_frame(frame_encode)).pack(pady=20)
Button(frame_start, text="Vyřešit šifru", font=("Font", 20), command=lambda: show_frame(frame_decode)).pack(pady=20)

# --- Okno pro vyřešení ---
Button(frame_decode, text="Vybrat vstupní soubor", font=("Font", 20), height=1, width=20, command=vyber_soubor).pack(pady=20)

# Rozpoznání šifry
t1 = Label(frame_decode, text="Šifra nerozpoznána", background="white", font=("Font", 20))
t1.pack()
Button(frame_decode, text="Rozpoznat šifru", font=("Font", 20), height=1, width=20, command=lambda: reseni.rozpoznat(t1, img) if img else t1.config(text="Nezvolen žádný obrázek")).pack(pady=20)

# Vyřešení šifry
t2 = Label(frame_decode, text="Šifra nevyřešena", background="white", font=("Font", 20))
t2.pack()
Button(frame_decode, text="Vyřešit šifru", font=("Font", 20), height=1, width=20, command=lambda: reseni.vyresit(t2, img=img, rozpoznano_label=t1)).pack(pady=20)
Button(frame_decode, text="Zpět na původní obrazovku", font=("Font", 20), command=lambda: show_frame(frame_start)).pack(pady=20)

# --- Okno pro zašifrování šifry ---
Label(frame_encode, text="Zadejte text pro zašifrování", background="white", font=("Font", 20)).pack(pady=20)
inputtxt = Text(frame_encode, height = 10, width = 40, bg = "light yellow")
inputtxt.pack(pady=20)

#Výběr šifry
vyber = StringVar()
vyber.set("Vyber druh šifry")

polozky = os.listdir("fonty")

nabidka = OptionMenu(frame_encode, vyber, *polozky)
nabidka.config(font=("Font", 20))
nabidka["menu"].config(font=("Font", 20))
nabidka.pack(pady=20)

t3 = Label(frame_encode, text="Šifra nevybrána!", background="white", font=("Font", 20), fg="red")

#Zašifrování
Button(frame_encode, text="Vybrat", font=("Font", 20), command=potvrdit).pack(pady=20)
Button(frame_encode, text ="Zašifrovat text", font=("Font", 20), command = lambda:Take_input(vybrany_font)).pack(pady=20)
Button(frame_encode, text="Zpět na původní obrazovku", font=("Font", 20), command=lambda: show_frame(frame_start)).pack(pady=20)

show_frame(frame_start)
root.mainloop()