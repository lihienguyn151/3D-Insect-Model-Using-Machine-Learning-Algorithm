# Enhance 3D Insect Models using Machine Learning Algorithm
***🔥Project Status:** Updating... (2026)*

---
✨**My Greetings:**

This is the source code for my graduation thesis. My name is Nguyen, an 4-year student in the Faculty of Information Technology at An Giang University, VNU-HCM, check!!!

---
🌟**INTRODUCTION**

---
📌**TABLE OF CONTENTS**

(a) Pre-Processing Image

---
💫**Pre-Processing Image**

This folder is utilized for storing the pre-processing source code that contains:

- AnyLabeling + Background Removal: masking algorithm.
- U-Net + VGG16 architecture: train + evaluation + model + utils.
- Mask prediction .py file.

*(a1) Masking Algorithm*

To create the ground-truth masks as well as the datasets removed background, firstly, AnyLabeling is utilized to draw the polygonal label that covers fully the insect body so that the label file can be rendered. Using the binary mask with the respectively image, a target image is exported that concentrates on the interest object.

The folder structure is presented in this following section:

|-- [images]

|-- [labels]

|-- [masks]

|-- **masking_algorithm.py**

Some necessary packages must be installed to run this program. This following present the packages for execution:

```bash
pip install opencv-python
pip install numpy
pip install tqdm
```

Subsequently, the setting modality to predict the mask using checkpoint file is denoted:

*(a2) Mask Prediction*

The workflow begin with the reading task to "images" and "masks" folder. From the "checkpoints" folder, a fully trained model can be imported in this program. After completely loading, a binary mask array is predicted from each images so that the mask can be rendered for the input dataset.  

