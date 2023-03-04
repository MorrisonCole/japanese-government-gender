import os
import re

import cv2

from configuration import IMAGES_FOLDER

female = 'female'
male = 'male'

for image_filename in os.listdir(IMAGES_FOLDER):
    if re.match(f"^({female}|{male}).*", image_filename):
        print(f"Skipping {image_filename}")
        continue

    imagePath = os.path.join(IMAGES_FOLDER, image_filename)
    image = cv2.imread(imagePath)

    cv2.imshow(image_filename, image)
    key = cv2.waitKeyEx()

    if key == 2424832:
        gender = female
    elif key == 2555904:
        gender = male
    else:
        break

    os.rename(imagePath, os.path.join(IMAGES_FOLDER, f"{gender}-{image_filename}"))
