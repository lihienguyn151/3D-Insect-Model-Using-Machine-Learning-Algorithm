#Import library
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os
from tqdm import tqdm

from MainProgram import MakeFormCenter
import IntroductionForm
import VisualizationForm
import scripts.ObjectSegmentation as S

import torch
from unet.model import UNet

#Parameters
MODEL_PATH = "data/checkpoints/checkpoint_epoch100_FT4.pth"
SCALE_FACTOR = 0.5
MASK_THRESHOLD = 0.5
NUM_CLASSES = 2
BILINEAR = True

#Form definition
class SegmentationForm:
    def __init__(self):
        self.form = tk.Tk()

        self.form.title("Phân đoạn ảnh")
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

        self.btnSegment = tk.Button(self.fMenu, text = "Phân đoạn ảnh", font = ("Times New Roman", 13, "bold"), width = 14, height = 1, bg = "#fffbdf", fg = "#833812", command = self.btnSegment_Click)
        self.btnSegment.place(x = 105, y = 3)

        self.btnVisualize = tk.Button(self.fMenu, text = "Trực quan 3D", font = ("Times New Roman", 13), width = 14, height = 1, bg = "#ffffff", fg = "#833812", command = self.btnVisualize_Click)
        self.btnVisualize.place(x = 257, y = 3)

        #Main content
        #1. Choose the segmentation option
        self.lbOption = tk.Label(self.form, text = "Tùy chọn phân đoạn", font = ("Times New Roman", 13, "bold"), bg = "#fff6e5", fg = "#762908")
        self.lbOption.place(x = 10, y = 156)

        self.fOption = tk.Frame(self.form, width = 315, height = 41, relief = "solid", bg = "#ffffff")
        self.fOption.place(x = 165, y = 150)

        self.btnEachImg = tk.Button(self.fOption, text = "Một ảnh", font = ("Times New Roman", 12, "bold"), bg = "#6e3e25", fg = "#ffffff", width = 14, command = self.btnEachImg_Click)
        self.btnEachImg.place(x = 20, y = 4)

        self.btnImgFolder = tk.Button(self.fOption, text = "Thư mục ảnh", font = ("Times New Roman", 12, "bold"), bg = "#6e3e25", fg = "#ffffff", width = 14, command = self.btnImgFolder_Click)
        self.btnImgFolder.place(x = 160, y = 4)

        #2. Segmentation one image
        self.lbOption1 = tk.Label(self.form, text = "    Phân đoạn một ảnh    ", font = ("Times New Roman", 13, "bold"), bg = "#ffffff", fg = "#762908", height = 2)
        self.lbOption1.place(x = 10, y = 203)

        self.fEachImg = tk.Frame(self.form, width = 750, height = 410, relief = "flat", bg = "#ffffff", borderwidth = 1)
        self.fEachImg.place(x = 10, y = 238)

        self.lfInput = tk.LabelFrame(self.fEachImg, width = 253, height = 380, relief = "solid", borderwidth = 1)
        self.lfInput.place(x = 40, y = 15)
        self.lfInput.pack_propagate(False)

        self.cvInput = tk.Canvas(self.lfInput, width = 253, height = 380, highlightthickness = 0)
        self.cvInput.pack(anchor = "center")
        self.ImportImage = ""
        self.piInput = ""

        self.lfOutput = tk.LabelFrame(self.fEachImg, width = 253, height = 380, relief = "solid", borderwidth = 1)
        self.lfOutput.place(x = 457, y = 15)
        self.lfOutput.pack_propagate(False)

        self.cvOutput = tk.Canvas(self.lfOutput, width = 253, height = 380, highlightthickness = 0)
        self.cvOutput.pack(anchor = "center")
        self.piOutput = ""

        self.btnImport = tk.Button(self.fEachImg, text = "Nhập ảnh", font = ("Times New Roman", 13, "bold"), width = 11, height = 1, bg = "#fffbdf", fg = "#833812", state = "disabled", command = self.btnImport_Click)
        self.btnImport.place(x = 315, y = 110)

        self.btnChangeDir = tk.Button(self.fEachImg, text = "Đổi thư mục", font = ("Times New Roman", 13, "bold"), width = 11, height = 1, bg = "#fffbdf", fg = "#833812", state = "disabled", command = self.btnChangeDir_Click)
        self.btnChangeDir.place(x = 315, y = 160)
        self.DftOutputDir = "data/output"

        self.btnSegmentImg = tk.Button(self.fEachImg, text = "Phân đoạn", font = ("Times New Roman", 13, "bold"), width = 11, height = 1, bg = "#fffbdf", fg = "#833812", state = "disabled", command = self.btnSegmentImg_Click)
        self.btnSegmentImg.place(x = 315, y = 210)

        self.btnReset = tk.Button(self.fEachImg, text = "Đặt lại", font = ("Times New Roman", 13, "bold"), width = 11, height = 1, bg = "#fffbdf", fg = "#833812", state = "disabled", command = self.btnReset_Click)
        self.btnReset.place(x = 315, y = 260)

        #3. Segmentation image folder
        self.lbOption2 = tk.Label(self.form, text = "   Phân đoạn thư mục ảnh   ", font = ("Times New Roman", 13, "bold"), bg = "#ffffff", fg = "#762908", height = 2)
        self.lbOption2.place(x = 770, y = 203)

        self.fImgFolder = tk.Frame(self.form, width = 420, height = 410, relief = "flat", bg = "#ffffff", borderwidth = 1)
        self.fImgFolder.place(x = 770, y = 238)

        self.btnChangeImgDir = tk.Button(self.fImgFolder, text = "Chọn thư mục", font = ("Times New Roman", 13, "bold"), width = 11, height = 1, bg = "#fffbdf", fg = "#833812", state = "disabled", command = self.btnChangeImgDir_Click)
        self.btnChangeImgDir.place(x = 20, y = 10)
        self.ImgDir = "data/images"

        self.btnChangeOutputDir = tk.Button(self.fImgFolder, text = "Lưu vào nơi", font = ("Times New Roman", 13, "bold"), width = 11,height = 1, bg = "#fffbdf", fg = "#833812", state = "disabled", command = self.btnChangeOutputDir_Click)
        self.btnChangeOutputDir.place(x = 151, y = 10)
        self.OutputDir = "data/results"

        self.btnSegmentImgFolder = tk.Button(self.fImgFolder, text = "Phân đoạn", font = ("Times New Roman", 13, "bold"), width = 11, height = 1, bg = "#fffbdf", fg = "#833812", state = "disabled", command = self.btnSegmentImgFolder_Click)
        self.btnSegmentImgFolder.place(x = 282, y = 10)

        self.txtExeLog = tk.Text(self.fImgFolder, font = ("Times New Roman", 13), width = 42, height = 15, relief = "solid", borderwidth = 1, state = "disabled")
        self.txtExeLog.place(x = 20, y = 60)

        self.btnResetLog = tk.Button(self.fImgFolder, text = "Đặt lại", font = ("Times New Roman", 13, "bold"), width = 11, height = 1, bg = "#fffbdf", fg = "#833812", state = "disabled", command = self.btnResetLog_Click)
        self.btnResetLog.place(x = 151, y = 365)

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
        GUI = SegmentationForm()

    def btnVisualize_Click(self):
        self.form.destroy()
        GUI = VisualizationForm.VisualizationForm()

    def btnEachImg_Click(self):
        if (self.btnImport["state"] == "disabled"):
            self.btnImport.configure(state = "normal")
            self.btnChangeDir.configure(state = "normal")
        else:
            self.btnSegmentImg.configure(state = "disabled")
            self.btnReset.configure(state = "disabled")
        self.piInput = ""
        self.piOutput = ""
        self.btnChangeImgDir.configure(state = "disabled")
        self.btnChangeOutputDir.configure(state = "disabled")
        self.btnSegmentImgFolder.configure(state = "disabled")
        self.btnResetLog.configure(state = "disabled")

    def btnImgFolder_Click(self):
        if (self.btnChangeImgDir["state"] == "disabled"):
            self.btnChangeImgDir.configure(state = "normal")
            self.btnChangeOutputDir.configure(state = "normal")
        else:
            self.btnSegmentImgFolder.configure(state = "disabled")
            self.btnResetLog.configure(state = "disabled")
        self.btnImport.configure(state = "disabled")
        self.btnChangeDir.configure(state = "disabled")
        self.btnSegmentImg.configure(state = "disabled")
        self.btnReset.configure(state = "disabled")
        self.piInput = ""
        self.piOutput = ""

    def btnImport_Click(self):
        image_path = filedialog.askopenfilename(filetypes=[("Chọn một ảnh EDOF côn trùng", "*.jpg *.jpeg *.png *.bmp")])

        image = Image.open(image_path)
        self.ImportImage = image_path

        image = image.resize((253, 380), Image.LANCZOS)
        self.piInput = ImageTk.PhotoImage(image)
        self.cvInput.create_image(0, 0, anchor = "nw", image = self.piInput)

        if (self.piInput != ""):
            self.btnSegmentImg.configure(state = "normal")
            self.btnReset.configure(state = "normal")

    def btnChangeDir_Click(self):
        temp = self.DftOutputDir
        self.DftOutputDir = filedialog.askdirectory()
        messagebox.showinfo("Thông báo", "Đã chuyển vị trí lưu ảnh phân đoạn từ '" + temp + "' sang '" + str(self.DftOutputDir) + "'!")

    def btnSegmentImg_Click(self):
        result_path = S.SegmentImage(self.ImportImage, self.DftOutputDir)
        image = Image.open(result_path)
        image = image.resize((253, 380), Image.LANCZOS)
        self.piOutput = ImageTk.PhotoImage(image)
        self.cvOutput.create_image(0, 0, anchor = "nw", image = self.piOutput)
        messagebox.showinfo("Thông báo", "Đã lưu mặt nạ và kết quả phân đoạn theo đường dẫn: " + str(result_path) + "!")

    def btnReset_Click(self):
        self.piInput = ""
        self.ImportImage = ""

        self.piOutput = ""

        self.DftOutputDir = "data/output"
        self.btnSegmentImg.configure(state = "disabled")
        self.btnReset.configure(state = "disabled")

    def btnChangeImgDir_Click(self):
        self.ImgDir = filedialog.askdirectory()
        messagebox.showinfo("Thông báo", "Đã điều chỉnh vị trí lưu tập ảnh EDOF đầu vào sang đường dẫn: '" + str(self.ImgDir) + "'!")

        if (self.ImgDir):
            self.btnSegmentImgFolder.configure(state = "normal")
            self.btnResetLog.configure(state = "normal")

    def btnChangeOutputDir_Click(self):
        self.OutputDir = filedialog.askdirectory()
        messagebox.showinfo("Thông báo", "Đã điều chỉnh vị trí xuất kết quả sang đường dẫn: '" + str(self.OutputDir) + "'!")

    def btnSegmentImgFolder_Click(self):
        #Folder configuration
        os.makedirs(self.OutputDir, exist_ok = True)
        image_files = [f for f in os.listdir(self.ImgDir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tif"))]

        #Setup environment
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        #Model loading
        net = UNet(n_channels = 3, n_classes = NUM_CLASSES, bilinear = BILINEAR)
        net.to(device)
        state_dict = torch.load(MODEL_PATH, map_location = device)
        state_dict.pop("mask_values", None)
        net.load_state_dict(state_dict)

        #Logging
        self.txtExeLog.configure(state = "normal")
        self.txtExeLog.insert(tk.END, f"<*> Trong thư mục có {len(image_files)} ảnh.\n")

        #Main manipulation loop
        self.txtExeLog.insert(tk.END, f"<*> Bắt đầu phân đoạn thư mục ảnh EDOF:\n")
        num_image = 1
        for image_file in tqdm(image_files, desc="Segmenting"):
            image_path = os.path.join(self.ImgDir, image_file)
            result_path = S.SegmentImageForFolder(device, net, image_file, image_path, self.OutputDir)

            self.txtExeLog.insert(tk.END, f">>> Đã phân đoạn xong ảnh thứ {num_image}!\n")
            num_image += 1

        self.txtExeLog.insert(tk.END, f"<*> Hoàn tất tác vụ phân đoạn thư mục ảnh!\n")
        self.txtExeLog.configure(state = "disabled")
        messagebox.showinfo("Thông báo", "Đã hoàn thành phân đoạn thư mục ảnh với kết quả được lưu tại thư mục: '" + str(self.OutputDir) + "'!")

    def btnResetLog_Click(self):
        self.ImgDir = "data/images"
        self.OutputDir = "data/results"

        self.txtExeLog.configure(state = "normal")
        self.txtExeLog.delete(1.0, tk.END)
        self.txtExeLog.configure(state = "disabled")

        self.btnSegmentImgFolder.configure(state = "disabled")
        self.btnResetLog.configure(state = "disabled")