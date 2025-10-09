from tkinter import Label
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

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