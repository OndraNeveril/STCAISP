from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import reseni

input_file = None

root = Tk()
root.title("Decoder")
root.configure(background="white")
root.attributes("-fullscreen", False)

Button(root, text="Vybrat vstupní soubor", font=("Font", 20), height = 1, width = 20, command=lambda: reseni.vstup(input_file, root)).pack(pady=20)

t1 = Label(root, text="Šifra nerozpoznána", background="white", font=("Font", 10))
t1.pack()
Button(root, text="Rozpoznat šifru", font=("Font", 20), height = 1, width = 20, command=lambda: reseni.rozpoznat(t1)).pack(pady=20)

t2 = Label(root, text="Šifra nevyřešena", background="white", font=("Font", 10))
t2.pack()
Button(root, text="Vyřešit šifru", font=("Font", 20), height = 1, width = 20, command=lambda: reseni.vyresit(t2)).pack(pady=20)

root.mainloop()