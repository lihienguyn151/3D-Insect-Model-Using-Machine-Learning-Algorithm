#Import library
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

from MainProgram import MakeFormCenter
import SegmentationForm
import VisualizationForm

#Form definition
class IntroductionForm:
    def __init__(self):
        self.form = tk.Tk()

        self.form.title("Lời giới thiệu")
        self.form.geometry("1200x700")
        self.form.configure(bg = "#ffffff")

        #Header design
        self.lfHeader = tk.LabelFrame(self.form, width = 1200, height = 100)
        self.lfHeader.place(x = 0, y = 0)
        self.lfHeader.pack_propagate(False)

        self.cvHeader = tk.Canvas(self.lfHeader, width = 1200, height = 100, highlightthickness = 0)
        self.cvHeader.pack(anchor = "center")
        image_path = "images/VisualHeader.png"
        image = Image.open(image_path)
        self.piHeader = ImageTk.PhotoImage(image)
        self.cvHeader.create_image(600, 45, image = self.piHeader)

        #Menu list
        self.fMenu = tk.Frame(self.form, width = 1200, height = 40, relief = "flat", bg = "#9a5300")
        self.fMenu.place(x = 0, y = 100)

        self.btnIntro = tk.Button(self.fMenu, text = "Giới thiệu", font = ("Times New Roman", 13, "bold"), width = 10, height = 1, bg = "#fffbdf", fg = "#833812", command = self.btnIntro_Click)
        self.btnIntro.place(x = 3, y = 3)

        self.btnSegment = tk.Button(self.fMenu, text = "Phân đoạn ảnh", font = ("Times New Roman", 13), width = 14, height = 1, bg = "#ffffff", fg = "#833812", command = self.btnSegment_Click)
        self.btnSegment.place(x = 115, y = 3)

        self.btnVisualize = tk.Button(self.fMenu, text = "Trực quan 3D", font = ("Times New Roman", 13), width = 14, height = 1, bg = "#ffffff", fg = "#833812", command = self.btnVisualize_Click)
        self.btnVisualize.place(x = 253, y = 3)

        #Main content
        self.lfContent = tk.LabelFrame(self.form, width = 1200, height = 520)
        self.lfContent.place(x = 0, y = 141)
        self.lfContent.pack_propagate(False)

        self.cvContent = tk.Canvas(self.lfContent, width = 1200, height = 520, highlightthickness = 0)
        self.cvContent.pack(anchor = "center")
        image_path = "images/IntroductionContent.png"
        image = Image.open(image_path)
        self.piContent = ImageTk.PhotoImage(image)
        self.cvContent.create_image(600, 258, image = self.piContent)

        #Footer
        self.lfFooter = tk.LabelFrame(self.form, width = 1200, height = 40)
        self.lfFooter.place(x = 0, y = 660)
        self.lfFooter.pack_propagate(False)

        self.cvFooter = tk.Canvas(self.lfFooter, width = 1200, height = 40, highlightthickness = 0)
        self.cvFooter.pack(anchor = "center")
        image_path = "images/VisualFooter.png"
        image = Image.open(image_path)
        self.piFooter = ImageTk.PhotoImage(image)
        self.cvFooter.create_image(600, 18, image = self.piFooter)

        MakeFormCenter(self.form)
        self.form.mainloop()

    def btnIntro_Click(self):
        self.form.destroy()
        GUI = IntroductionForm()

    def btnSegment_Click(self):
        self.form.destroy()
        GUI = SegmentationForm.SegmentationForm()

    def btnVisualize_Click(self):
        self.form.destroy()
        GUI = VisualizationForm.VisualizationForm()