#Library import
import os
import json
import cv2
import numpy as np
from tqdm import tqdm

#Parameters
JSON_DIR = r"labels"
OUTPUT_DIR = r"masks"

#Main program
if __name__=="__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    #Main loop
    for file in tqdm(os.listdir(JSON_DIR)):
        if not file.endswith(".json"):
            continue

        json_path = os.path.join(JSON_DIR, file)

        #Read .JSON file
        with open(json_path, "r") as f:
            data = json.load(f)

        #Read image files
        image_file, _ = os.path.splitext(file)
        image_path = "images/" + image_file + ".jpg"
        image = cv2.imread(image_path)
        if image is None:
            print(f"<*> Get the fault when reading image from this path: {image_path}!!!")
            continue

        #Create initial mask
        height, width = image.shape[0:2]
        mask = np.zeros((height, width, 3), dtype=np.uint8)

        #Masking each object segmentation region
        for shape in data["shapes"]:
            if shape["shape_type"] != "polygon":
                continue

            points = np.array(shape["points"], dtype=np.int32)
            points = points.reshape((-1, 1, 2))

            poly_mask = np.zeros((height, width), dtype=np.uint8)
            cv2.fillPoly(poly_mask, [points], 255)

            mask[poly_mask == 255] = image[poly_mask == 255]

        #Result saving
        out_path = os.path.join(OUTPUT_DIR, file.replace(".json", ".png"))
        cv2.imwrite(out_path, mask)

    print("<*> Completely execution.")