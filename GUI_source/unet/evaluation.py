#Evaluate performance
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms.functional as TF
from tqdm import tqdm
from unet.utils import multiclass_dice_coeff
import numpy as np

@torch.inference_mode()
def evaluate(net, dataloader, device, amp, last_epochs=False, num_classes=2):
    net.eval()
    criterion = nn.CrossEntropyLoss()

    #Evaluation
    total_loss = 0
    dice_total, iou_total, acc_total = 0, 0, 0
    precision_total, recall_total, f1_total = 0, 0, 0

    #Confusion matrix
    y_true_all, y_pred_all = [], []

    #Iterate over the validation set
    with torch.no_grad():
        for batch in tqdm(dataloader, total=len(dataloader), desc='Validation round', unit='batch', leave=False):
            image, mask_true = batch['image'], batch['mask']

            #Move images and labels to correct device and type
            image = image.to(device=device, dtype=torch.float32, memory_format=torch.channels_last)
            mask_true = mask_true.to(device=device, dtype=torch.long) #[B,H,W]

            with torch.autocast(device.type if device.type != 'mps' else 'cpu', enabled=amp):
                #Predict the mask
                logits = net(image) #[B,2,H,W]

                if logits.shape[-2:] != mask_true.shape[-2:]:
                    logits = TF.resize(logits,mask_true.shape[-2:],interpolation=TF.InterpolationMode.NEAREST)

                #Compute validation loss
                loss = criterion(logits, mask_true)
                total_loss += loss.item()

                #Prediction
                prediction = torch.argmax(logits, dim=1) #[B,H,W]
                if last_epochs:
                    y_true_all.append(mask_true.cpu().numpy())
                    y_pred_all.append(prediction.cpu().numpy())

                #Compute the Dice score, ignoring background
                dice_total += multiclass_dice_coeff(prediction, mask_true)

                #Compute accuracy
                acc_total += (prediction == mask_true).float().mean().item()

                #Metrics in object prediction
                pred_fg = (prediction == 1)
                true_fg = (mask_true == 1)

                #Compute IoU
                intersection = (pred_fg & true_fg).sum(dim=(1,2))
                union = (pred_fg | true_fg).sum(dim=(1,2))
                iou = (intersection + 1e-6) / (union + 1e-6)
                iou_total += iou.mean().item()

                #Compute Precision, Recall and F1-Score
                tp = intersection.float()
                fp = (pred_fg & ~true_fg).sum(dim=(1,2)).float()
                fn = (~pred_fg & true_fg).sum(dim=(1,2)).float()

                precision = tp / (tp + fp + 1e-6)
                recall = tp / (tp + fn + 1e-6)
                f1 = 2 * precision * recall / (precision + recall + 1e-6)

                precision_total += precision.mean().item()
                recall_total += recall.mean().item()
                f1_total += f1.mean().item()

    n = len(dataloader)
    return total_loss / n, dice_total / n, iou_total / n, acc_total / n, precision_total / n, recall_total / n, f1_total / n, np.array(y_true_all), np.array(y_pred_all)