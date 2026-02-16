#Library import
import os
from PIL import Image
import torch
from torch.utils.data import Dataset
from unet.utils import BasicDataset
from torch.utils.data import DataLoader
from unet.model import UNet
from evaluation import evaluate

#Class setting
class TestDataset(Dataset):
    def __init__(self, image_dir, mask_dir, scale=1.0, mask_values=[0,255]):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.scale = scale
        self.mask_values = mask_values

        self.images = sorted(os.listdir(image_dir))
        self.masks = sorted(os.listdir(mask_dir))

        assert len(self.images) == len(self.masks), "Image-mask count mismatch!"

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_dir, self.images[idx])
        mask_path = os.path.join(self.mask_dir, self.masks[idx])

        img = Image.open(img_path).convert('RGB')
        mask = Image.open(mask_path)

        img = BasicDataset.preprocess(self.mask_values, img, self.scale, is_mask=False)
        mask = BasicDataset.preprocess(self.mask_values, mask, self.scale, is_mask=True)

        return {
            'image': torch.as_tensor(img, dtype=torch.float32),
            'mask': torch.as_tensor(mask, dtype=torch.long)
        }

#Parameters
IMAGE_DIR = "../images"
MASK_DIR  = "../masks"
CHECKPOINT = "../checkpoints/checkpoint_epoch100_FT4.pth"
BATCH_SIZE = 4
NUM_CLASSES = 2
SCALE = 0.5
AMP = True

#Main program
if __name__=="__main__":
    #Data loading
    test_dataset = TestDataset(image_dir=IMAGE_DIR,mask_dir=MASK_DIR,scale=SCALE)
    test_loader = DataLoader(test_dataset,batch_size=BATCH_SIZE,shuffle=False,num_workers=2,pin_memory=True)

    #Model loading
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"<*> Using device: {device}")

    net = UNet(n_channels=3,n_classes=NUM_CLASSES,bilinear=True)
    state_dict = torch.load(CHECKPOINT, map_location=device)
    mask_values = state_dict.pop('mask_values', [0, 1])
    net.load_state_dict(state_dict)
    net.to(device)

    print("<*> Model loaded successfully!")

    #Evaluating in testing dataset
    (loss,dice,iou,acc,precision,recall,f1,y_true,y_pred) = evaluate(net=net,dataloader=test_loader,device=device,amp=AMP,last_epochs=False,num_classes=NUM_CLASSES)

    #Display testing results
    print("\n<*> Test results:")
    print(f"Loss: {loss:.4f}")
    print(f"Dice's Coefficient: {dice:.4f}")
    print(f"IoU: {iou:.4f}")
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")