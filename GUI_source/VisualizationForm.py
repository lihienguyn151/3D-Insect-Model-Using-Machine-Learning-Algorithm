#Import library
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

from MainProgram import MakeFormCenter
import IntroductionForm
import SegmentationForm

from pyopengltk import OpenGLFrame
from OpenGL.GL import *
import trimesh

#Function settings
class Viewer(OpenGLFrame):
    def __init__(self, parent, mesh, **kwargs):
        super().__init__(parent, **kwargs)

        self.mesh = mesh
        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces

    def initgl(self):
        glClearColor(1, 1, 1, 1)
        glEnable(GL_DEPTH_TEST)

    def redraw(self):
        if self.faces is None:
            return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()


#Form definition
class VisualizationForm:
    def __init__(self):
        self.form = tk.Tk()

        self.form.title("Trực quan mô hình 3D")
        self.form.geometry("1200x700")
        self.form.configure(bg = "#fff6e5")

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

        self.btnIntro = tk.Button(self.fMenu, text = "Giới thiệu", font = ("Times New Roman", 13), width = 10, height = 1, bg = "#ffffff", fg = "#833812", command = self.btnIntro_Click)
        self.btnIntro.place(x = 3, y = 3)

        self.btnSegment = tk.Button(self.fMenu, text = "Phân đoạn ảnh", font = ("Times New Roman", 13), width = 14, height = 1, bg = "#ffffff", fg = "#833812", command = self.btnSegment_Click)
        self.btnSegment.place(x = 105, y = 3)

        self.btnVisualize = tk.Button(self.fMenu, text = "Trực quan 3D", font = ("Times New Roman", 13, "bold"), width = 14, height = 1, bg = "#fffbdf", fg = "#833812", command = self.btnVisualize_Click)
        self.btnVisualize.place(x = 243, y = 3)

        #Main content
        #1. Model view option
        self.mbModelView = tk.Menubutton(self.form, text = "Chọn mô hình", font = ("Times New Roman", 13, "bold"), bg = "#ffffff", fg = "#833812", relief = "solid", borderwidth = 1)
        self.mbModelView.place(x = 10, y = 148)

        self.mnuModelView = tk.Menu(self.mbModelView, tearoff = 0)
        self.mbModelView.config(menu = self.mnuModelView)

        self.mnuModelView.add_command(label = "Achroia grisella", font = ("Times New Roman", 12), command = self.mnuSample01_Click)
        self.mnuModelView.add_command(label = "Amblypelta nitida", font = ("Times New Roman", 12), command = self.mnuSample02_Click)
        self.mnuModelView.add_command(label = "Amphimallon solstitiale", font = ("Times New Roman", 12), command = self.mnuSample03_Click)
        self.mnuModelView.add_command(label = "Cerambycidae", font = ("Times New Roman", 12), command = self.mnuSample04_Click)
        self.mnuModelView.add_command(label = "Chlorocala Africana", font = ("Times New Roman", 12), command = self.mnuSample05_Click)
        self.mnuModelView.add_command(label = "Hemiptera", font = ("Times New Roman", 12), command = self.mnuSample06_Click)
        self.mnuModelView.add_command(label = "Hypomeces squamosus", font = ("Times New Roman", 12), command = self.mnuSample07_Click)
        self.mnuModelView.add_command(label = "Pyrrhocoris apterus", font = ("Times New Roman", 12), command = self.mnuSample08_Click)

        #2. Visualize 3D model
        self.fVisualize = tk.Frame(self.form, width = 800, height = 467, relief = "solid", borderwidth = 1)
        self.fVisualize.place(x = 10, y = 183)

        self.lbManeuver = tk.Label(self.form, text = "Bảng chức năng", font = ("Times New Roman", 14, "bold"), bg = "#fff6e5", fg = "#833812")
        self.lbManeuver.place(x = 835, y = 152)

        self.fManeuver = tk.Frame(self.form, width = 365, height = 467, relief = "solid", borderwidth = 1, bg = "#ffffff")
        self.fManeuver.place(x = 825, y = 183)
        self.vrSample = None

        self.btnOpen = tk.Button(self.fManeuver, text = "Mở tập tin", font = ("Times New Roman", 13, "bold"), width = 32, height = 1, bg = "#fffbdf", fg = "#833812", command = self.btnOpen_Click)
        self.btnOpen.place(x = 17, y = 20)

        self.btnReset = tk.Button(self.fManeuver, text = "Đặt lại", font = ("Times New Roman", 13, "bold"), width = 32, height = 1, bg = "#fffbdf", fg = "#833812", state = "disabled", command = self.btnReset_Click)
        self.btnReset.place(x = 17, y = 70)

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
        GUI = IntroductionForm.IntroductionForm()

    def btnSegment_Click(self):
        self.form.destroy()
        GUI = SegmentationForm.SegmentationForm()

    def btnVisualize_Click(self):
        self.form.destroy()
        GUI = VisualizationForm()

    def mnuSample01_Click(self):
        model_path = "data/models/Achroia_grisella_NeRF.obj"
        mesh = trimesh.load(model_path)
        self.vrSample = Viewer(self.fVisualize, mesh, width = 800, height = 467)
        self.vrSample.pack(fill = "both", expand = True)
        self.vrSample.animate = 0
        self.btnReset.configure(state = "normal")

    def mnuSample02_Click(self):
        model_path = "data/models/Amblypelta_nitida_NeRF.obj"
        mesh = trimesh.load(model_path)
        self.vrSample = Viewer(self.fVisualize, mesh, width = 800, height = 467)
        self.vrSample.pack(fill = "both", expand = True)
        self.vrSample.animate = 0
        self.btnReset.configure(state = "normal")

    def mnuSample03_Click(self):
        model_path = "data/models/Amphimallon_NeRF.obj"
        mesh = trimesh.load(model_path)
        self.vrSample = Viewer(self.fVisualize, mesh, width = 800, height = 467)
        self.vrSample.pack(fill = "both", expand = True)
        self.vrSample.animate = 0
        self.btnReset.configure(state = "normal")

    def mnuSample04_Click(self):
        model_path = "data/models/Cerambycidae_NeRF.obj"
        mesh = trimesh.load(model_path)
        self.vrSample = Viewer(self.fVisualize, mesh, width = 800, height = 467)
        self.vrSample.pack(fill = "both", expand = True)
        self.vrSample.animate = 0
        self.btnReset.configure(state = "normal")

    def mnuSample05_Click(self):
        model_path = "data/models/Chlorocala_NeRF.obj"
        mesh = trimesh.load(model_path)
        self.vrSample = Viewer(self.fVisualize, mesh, width = 800, height = 467)
        self.vrSample.pack(fill = "both", expand = True)
        self.vrSample.animate = 0
        self.btnReset.configure(state = "normal")

    def mnuSample06_Click(self):
        model_path = "data/models/Hemiptera_NeRF.obj"
        mesh = trimesh.load(model_path)
        self.vrSample = Viewer(self.fVisualize, mesh, width = 800, height = 467)
        self.vrSample.pack(fill = "both", expand = True)
        self.vrSample.animate = 0
        self.btnReset.configure(state = "normal")

    def mnuSample07_Click(self):
        model_path = "data/models/Hypomeces_NeRF.obj"
        mesh = trimesh.load(model_path)
        self.vrSample = Viewer(self.fVisualize, mesh, width = 800, height = 467)
        self.vrSample.pack(fill = "both", expand = True)
        self.vrSample.animate = 0
        self.btnReset.configure(state = "normal")

    def mnuSample08_Click(self):
        model_path = "data/models/Pyrrhocoris_NeRF.obj"
        mesh = trimesh.load(model_path)
        self.vrSample = Viewer(self.fVisualize, mesh, width = 800, height = 467)
        self.vrSample.pack(fill = "both", expand = True)
        self.vrSample.animate = 0
        self.btnReset.configure(state = "normal")

    def btnOpen_Click(self):
        model_path = filedialog.askopenfilename(filetypes = [("Chọn một tập tin mô hình 3D", "*.obj *.ply")])
        mesh = trimesh.load(model_path)
        self.vrSample = Viewer(self.fVisualize, mesh, width = 800, height = 467)
        self.vrSample.pack(fill = "both", expand = True)
        self.vrSample.animate = 0
        self.btnReset.configure(state = "normal")

    def btnReset_Click(self):
        self.vrSample = None
        self.btnReset.configure(state = "disabled")