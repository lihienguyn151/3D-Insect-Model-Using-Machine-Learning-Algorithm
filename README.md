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

📂The folder structure is presented in this following section:

```text
pre_processing/
├── images/
├── labels/
├── masks/       
└── masking_algorithm.py
```

Some necessary packages must be installed to run this program. This following present the packages for execution:

```bash
pip install opencv-python
pip install numpy
pip install tqdm
```

*(a2) U-Net Architecture*

This setup consists of four main source code for training task like model, utils, evaluation and train. The U-Net Architecture that contains VGG16 layers as the encoder is written in *model.py*. In this file, the initial number of feature channel can be changed for some test-case, 32 or 64.

The *utils.py* file gives some function for dataset creation, image pre-processing and dice loss function computation. The evaluation code is utilized to compute the performance metrics, such as DsC, IoU, evaluation loss and general accuracy.

Some hyper-parameters can be fine-tunned in the main function of *train.py* file. The parameters that are used in my source code, are gained the default value: 1e-4 for the learning rate, 0.1 for validation sample size, 16 for batch size, and true for bilinear and amp. When training, this source integrates with the others to train the U-Net model.

Moreover, the *prediction.py* file can be used to test the model by checkpoints loading, image importation and mask prediction.

📂The following section presents the folder structure for run the training scripts:

```text
pre_processing/
├── checkpoints/
├── images/
├── masks/
├── metrics/
├── test/
├── unet/
│   ├── evaluation.py          
│   ├── model.py
│   ├── prediction.py
│   ├── train.py
│   └── utils.py        
└── mask_prediction.py
```

Some libraries and packages must be installed in the configuration environment by running this script:

```bash
pip3 install sympy==1.12
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
pip install matplotlib
pip install numpy
pip install Pillow
pip install tqdm
pip install wandb
pip install albumentations
```

However, these setting aren't necessary when using my Google Colaboratory for training model. This can be accessed in [U-Net+VGG16 Notebook](https://colab.research.google.com/drive/1eLcUQTXZGMWJKd_MCuSoJKFX82PbEG03?usp=sharing).

Subsequently, the setting modality to predict the mask using checkpoint file is denoted:

*(a3) Mask Prediction*

The workflow begins with the reading task to "images" and "masks" folder. From the "checkpoints" folder, a fully trained model can be imported in this program. After completely loading, a binary mask array is predicted from each images so that the mask can be rendered for the input dataset. This source supports for both CPU and GPU Cuda. 

📂The data structure that is utilized by the automatically mask prediction using U-Net model is:

```text
pre_processing/
├── checkpoints/
│   └── checkpoint_epoch100_FT4.pth
├── images/
├── masks/
├── results/
├── unet/
│   ├── evaluation.py          
│   ├── model.py
│   ├── prediction.py
│   ├── train.py
│   └── utils.py        
└── mask_prediction.py
```

Therefore, the machine learning libraries are necessary to load the U-Net model and trained weights.
