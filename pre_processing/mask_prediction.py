#Library import
import os
import logging
import numpy as np
import torch
import torch.nn.functional as F
import cv2
from PIL import Image
from tqdm import tqdm

from unet.utils import BasicDataset
from unet.model import UNet

#Parameters
MODEL_PATH = "./checkpoints/checkpoint_epoch100_FT4.pth"
IMAGE_DIR = "./images"
MASK_DIR = "./masks"
RESULT_DIR = "./results"

SCALE_FACTOR = 0.5
MASK_THRESHOLD = 0.5
NUM_CLASSES = 2
BILINEAR = True

#Function settings
def predict_img(net, full_img, device, scale_factor=1.0, out_threshold=0.5):
    net.eval()

    img = torch.from_numpy(BasicDataset.preprocess(None, full_img, scale_factor, is_mask=False))
    img = img.unsqueeze(0).to(device=device, dtype=torch.float32)

    with torch.no_grad():
        output = net(img)
        output = F.interpolate(output,size=(full_img.size[1], full_img.size[0]),mode='bilinear',align_corners=False
        )

        if net.n_classes > 1:
            mask = output.argmax(dim=1)
        else:
            mask = torch.sigmoid(output) > out_threshold
    return mask[0].cpu().numpy().astype(np.uint8)


def mask_to_image(mask: np.ndarray):
    mask = mask * 255
    return Image.fromarray(mask.astype(np.uint8))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    os.makedirs(MASK_DIR, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"<*> Using device: {device}")

    #Load model
    net = UNet(n_channels=3, n_classes=NUM_CLASSES, bilinear=BILINEAR)
    net.to(device)

    state_dict = torch.load(MODEL_PATH, map_location=device)
    state_dict.pop("mask_values", None)
    net.load_state_dict(state_dict)
    logging.info("<*> Model loaded successfully!")

    #List images
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tif"))]

    logging.info(f"<*> Found {len(image_files)} images.....")

    for fname in tqdm(image_files, desc="Segmenting"):
        img_path = os.path.join(IMAGE_DIR, fname)
        img = Image.open(img_path).convert("RGB")

        mask = predict_img(net=net, full_img=img, device=device, scale_factor=SCALE_FACTOR, out_threshold=MASK_THRESHOLD)

        mask_img = mask_to_image(mask)

        out_name = os.path.splitext(fname)[0] + "_mask.png"
        out_path = os.path.join(MASK_DIR, out_name)
        mask_img.save(out_path)

        #Combine mask in image respectively
        img = cv2.imread(img_path)
        mask = cv2.imread(out_path, cv2.IMREAD_GRAYSCALE)

        img2 = np.zeros_like(img)
        img2[:, :, 0] = mask
        img2[:, :, 1] = mask
        img2[:, :, 2] = mask

        result = cv2.bitwise_and(img, img2)
        result_name = os.path.splitext(fname)[0] + "_processed.png"
        result_path = os.path.join(RESULT_DIR, result_name)
        cv2.imwrite(result_path, result)

    logging.info("<*> All prediction images saved successfully!")