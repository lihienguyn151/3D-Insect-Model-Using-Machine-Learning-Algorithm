#Import library
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

import IntroductionForm

#Function setting
def MakeFormCenter(form):
    form.update_idletasks()
    width = form.winfo_width()
    height = form.winfo_height()

    x = (form.winfo_screenwidth() // 2) - (width // 2)
    y = (form.winfo_screenheight() // 2) - (height // 2) - 35

    form.geometry('{}x{}+{}+{}'.format(width, height, x, y))

#Main method
if __name__=="__main__":
    #Initialize introduction form
    GUI = IntroductionForm.IntroductionForm()