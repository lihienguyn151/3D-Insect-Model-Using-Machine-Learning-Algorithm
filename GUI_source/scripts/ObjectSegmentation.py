#Library import
import os
import numpy as np
import torch
import torch.nn.functional as F
import cv2
from PIL import Image
from tqdm import tqdm

from unet.utils import BasicDataset
from unet.model import UNet

#Parameters
MODEL_PATH = "./data/checkpoints/checkpoint_epoch100_FT4.pth"
SCALE_FACTOR = 0.5
MASK_THRESHOLD = 0.5
NUM_CLASSES = 2
BILINEAR = True

#Function settings
def PredictMask(net, full_img, device, scale_factor = 1.0, out_threshold = 0.5):
    net.eval()

    img = torch.from_numpy(BasicDataset.preprocess(None, full_img, scale_factor, is_mask = False))
    img = img.unsqueeze(0).to(device = device, dtype = torch.float32)

    with torch.no_grad():
        output = net(img)
        output = F.interpolate(output,size = (full_img.size[1], full_img.size[0]),mode = 'bilinear',align_corners = False)

        if net.n_classes > 1:
            mask = output.argmax(dim = 1)
        else:
            mask = torch.sigmoid(output) > out_threshold
    return mask[0].cpu().numpy().astype(np.uint8)


def MaskToImage(mask: np.ndarray):
    mask = mask * 255
    return Image.fromarray(mask.astype(np.uint8))

def SegmentImage(input_path, out_dir):
    #Setup environment
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    #Model loading
    net = UNet(n_channels = 3, n_classes = NUM_CLASSES, bilinear = BILINEAR)
    net.to(device)
    state_dict = torch.load(MODEL_PATH, map_location = device)
    state_dict.pop("mask_values", None)
    net.load_state_dict(state_dict)

    #Mask prediction
    input_image = Image.open(input_path).convert("RGB")
    mask = PredictMask(net = net, full_img = input_image, device = device, scale_factor = SCALE_FACTOR, out_threshold = MASK_THRESHOLD)
    mask_img = MaskToImage(mask)

    #Export mask
    output_mask = str(out_dir) + "/InsectMask.png"
    mask_img.save(output_mask)

    #Image integration
    input_image = cv2.imread(input_path)
    mask = cv2.imread(output_mask, cv2.IMREAD_GRAYSCALE)

    temp = np.zeros_like(input_image)
    temp[:, :, 0] = mask
    temp[:, :, 1] = mask
    temp[:, :, 2] = mask
    result = cv2.bitwise_and(input_image, temp)

    #Export segmentation image
    result_path = str(out_dir) + "/ImageSegmented.jpg"
    cv2.imwrite(result_path, result)

    return result_path

def SegmentImageForFolder(device, net, image_file, input_path, out_dir):
    #Mask prediction
    input_image = Image.open(input_path).convert("RGB")
    mask = PredictMask(net = net, full_img = input_image, device = device, scale_factor = SCALE_FACTOR, out_threshold = MASK_THRESHOLD)
    mask_img = MaskToImage(mask)

    #Export mask
    output_name = os.path.splitext(image_file)[0] + "_mask.png"
    output_mask = os.path.join(out_dir, output_name)
    mask_img.save(output_mask)

    #Image integration
    input_image = cv2.imread(input_path)
    mask = cv2.imread(output_mask, cv2.IMREAD_GRAYSCALE)

    temp = np.zeros_like(input_image)
    temp[:, :, 0] = mask
    temp[:, :, 1] = mask
    temp[:, :, 2] = mask
    result = cv2.bitwise_and(input_image, temp)

    #Export segmentation image
    result_name = os.path.splitext(image_file)[0] + "_processed.jpg"
    result_path = os.path.join(out_dir, result_name)
    cv2.imwrite(result_path, result)

    return result_path