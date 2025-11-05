from tkinter import *
from PIL import Image, ImageTk
import reseni

img = None           # PIL.Image objekt
img_label = None     # Label s obrázkem

root = Tk()
root.title("Decoder")
root.configure(background="white")
root.attributes("-fullscreen", False)

# --- Výběr souboru ---
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
        img_label = Label(root, image=display, bg="white")
        img_label.image = display
        img_label.pack()

Button(root, text="Vybrat vstupní soubor", font=("Font", 20),
       height=1, width=20, command=vyber_soubor).pack(pady=20)

# --- Rozpoznání šifry ---
t1 = Label(root, text="Šifra nerozpoznána", background="white", font=("Font", 10))
t1.pack()
Button(root, text="Rozpoznat šifru", font=("Font", 20),
       height=1, width=20,
       command=lambda: reseni.rozpoznat(t1, img) if img else t1.config(text="Nezvolen žádný obrázek")).pack(pady=20)

# --- Vyřešení šifry ---
t2 = Label(root, text="Šifra nevyřešena", background="white", font=("Font", 10))
t2.pack()
Button(root, text="Vyřešit šifru", font=("Font", 20), height=1, width=20,
       command=lambda: reseni.vyresit(t2)).pack(pady=20)

root.mainloop()
