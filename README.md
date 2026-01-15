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

- U-Net + VGG16 architecture: train + evaluation + model + utils.
- Mask prediction .py file.

Subsequently, the setting modality to predict the mask using checkpoint file is denoted:

*(a1) Mask Prediction*

The workflow begin with the reading task to "images" and "masks" folder. From the "checkpoints" folder, a fully trained model can be imported in this program. After completely loading, a binary mask array is predicted from each images so that the mask can be rendered for the input dataset.  

